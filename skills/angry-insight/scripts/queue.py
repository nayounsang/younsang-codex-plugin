#!/usr/bin/env python3
"""Local, opt-in prompt queue used by the angry-insight plugin skill."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import secrets
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

RETENTION = dt.timedelta(days=30)


def data_root() -> Path:
    value = os.environ.get("PLUGIN_DATA") or os.environ.get("CLAUDE_PLUGIN_DATA")
    if not value:
        raise RuntimeError("PLUGIN_DATA is unavailable; this plugin hook must run from Codex.")
    return Path(value).expanduser()


def now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def timestamp(value: dt.datetime | None = None) -> str:
    return (value or now()).isoformat(timespec="seconds").replace("+00:00", "Z")


def parse_time(value: Any) -> dt.datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return parsed.astimezone(dt.timezone.utc)
    except ValueError:
        return None


def project_root(cwd: str | None = None) -> str:
    path = Path(cwd or os.getcwd()).expanduser().resolve()
    try:
        result = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
            timeout=2,
        )
        return str(Path(result.stdout.strip()).resolve())
    except (OSError, subprocess.SubprocessError):
        return str(path)


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else None
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


def settings() -> dict[str, Any] | None:
    return read_json(data_root() / "settings.json")


def expire_pending(root: Path) -> int:
    """Delete expired pending records and abandoned atomic-write temp files."""
    pending = root / "pending"
    if not pending.exists():
        return 0
    cutoff = now() - RETENTION
    removed = 0
    for path in pending.iterdir():
        if not path.is_file():
            continue
        record = read_json(path) if path.suffix == ".json" else None
        captured = parse_time(record.get("captured_at")) if record else None
        try:
            # Temporary files may not contain parseable data; use mtime so a
            # crash during write cannot leave prompt fragments forever.
            expired = captured < cutoff if captured else dt.datetime.fromtimestamp(
                path.stat().st_mtime, tz=dt.timezone.utc
            ) < cutoff
            if expired:
                path.unlink()
                removed += 1
        except OSError:
            continue
    return removed


def current_scope_root(config: dict[str, Any], cwd: str | None = None) -> str:
    if config.get("scope") == "global":
        return "*"
    return str(config.get("project_root") or project_root(cwd))


def eligible(config: dict[str, Any] | None, cwd: str | None = None) -> bool:
    if not config or config.get("enabled") is not True:
        return False
    if config.get("scope") == "global":
        return True
    return config.get("scope") == "project" and config.get("project_root") == project_root(cwd)


def require_record_access(config: dict[str, Any] | None, record: dict[str, Any] | None = None) -> None:
    if not eligible(config):
        raise RuntimeError("Angry Insight is disabled or this event is outside the active scope.")
    if (
        record is not None
        and config is not None
        and config.get("scope") == "project"
        and record.get("project_root") != config.get("project_root")
    ):
        raise RuntimeError("Angry Insight is disabled or this event is outside the active scope.")


def validate_event_id(event_id: str) -> None:
    if not re.fullmatch(r"[0-9a-f]{32}", event_id):
        raise RuntimeError("Invalid event ID.")


def capture() -> None:
    try:
        event = json.load(sys.stdin)
        config = settings()
        if not isinstance(event, dict) or not eligible(config, event.get("cwd")):
            return
        prompt = event.get("prompt")
        session_id = event.get("session_id")
        turn_id = event.get("turn_id")
        if not isinstance(prompt, str) or not prompt.strip():
            return
        if not isinstance(session_id, str) or not isinstance(turn_id, str):
            return

        root = data_root()
        pending_dir = root / "pending"
        cases_dir = root / "cases"
        pending_dir.mkdir(parents=True, exist_ok=True)

        event_id = secrets.token_hex(16)
        record = {
            "event_id": event_id,
            "project_root": project_root(event.get("cwd")),
            "session_id": session_id,
            "turn_id": turn_id,
            "captured_at": timestamp(),
            "prompt_text": prompt,
            "transcript_path": event.get("transcript_path") if isinstance(event.get("transcript_path"), str) else None,
        }
        # Omit any accidental event ID collision with an existing result.
        if (cases_dir / f"{event_id}.json").exists():
            return
        atomic_json(pending_dir / f"{event_id}.json", record)
    except Exception as exc:
        # Fail open: a local capture problem must not block prompt submission.
        print(f"angry-insight capture skipped: {type(exc).__name__}", file=sys.stderr)


def extract_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                value = item.get("text")
                if isinstance(value, str):
                    parts.append(value)
        return "\n".join(part for part in parts if part)
    if isinstance(content, dict):
        return extract_text(content.get("text"))
    return ""


def transcript_messages(path: Path) -> list[tuple[str, str, str | None]]:
    """Read common transcript message shapes; format is intentionally best-effort."""
    messages: list[tuple[str, str, str | None]] = []
    try:
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not isinstance(entry, dict):
                    continue
                payload = entry.get("payload") if isinstance(entry.get("payload"), dict) else entry
                role = payload.get("role")
                if payload.get("type") == "message" and isinstance(payload.get("role"), str):
                    role = payload["role"]
                if role not in {"user", "assistant"}:
                    item_type = payload.get("type") or entry.get("type")
                    if item_type in {"user_message", "userMessage"}:
                        role = "user"
                    elif item_type in {"assistant_message", "assistantMessage"}:
                        role = "assistant"
                if role not in {"user", "assistant"}:
                    continue
                text = extract_text(payload.get("content"))
                if not text and isinstance(payload.get("message"), dict):
                    text = extract_text(payload["message"].get("content"))
                if not text:
                    text = extract_text(payload.get("text"))
                if text:
                    messages.append((role, text, payload.get("turn_id") if isinstance(payload.get("turn_id"), str) else None))
    except (OSError, UnicodeError):
        return []
    return messages


def inspect(event_id: str) -> None:
    validate_event_id(event_id)
    config = settings()
    require_record_access(config)
    root = data_root()
    record_path = root / "pending" / f"{event_id}.json"
    record = read_json(record_path)
    if not record or record.get("event_id") != event_id:
        raise RuntimeError("Pending event not found or invalid.")
    require_record_access(config, record)

    transcript_path = record.get("transcript_path")
    messages = transcript_messages(Path(transcript_path)) if isinstance(transcript_path, str) else []
    prompt = record.get("prompt_text", "")
    anchor = None
    for index, (role, text, turn_id) in enumerate(messages):
        if role == "user" and (text.strip() == prompt.strip() or turn_id == record.get("turn_id")):
            anchor = index
    candidates = messages[:anchor] if anchor is not None else messages
    previous = next((text for role, text, _ in reversed(candidates) if role == "assistant"), None)
    output = {
        "event_id": event_id,
        "project_root": record.get("project_root"),
        "captured_at": record.get("captured_at"),
        "prompt_text": prompt,
        "previous_assistant_response": previous,
        "transcript_match": anchor is not None,
    }
    print(json.dumps(output, ensure_ascii=False))


def list_pending() -> None:
    root = data_root()
    expire_pending(root)
    config = settings()
    if not config or config.get("enabled") is not True:
        print("[]")
        return
    scope = current_scope_root(config)
    eligible_records: list[tuple[str, Path, dict[str, Any]]] = []
    for path in sorted((root / "pending").glob("*.json")) if (root / "pending").exists() else []:
        item = read_json(path)
        if not item or not isinstance(item.get("event_id"), str):
            continue
        if scope == "*" or item.get("project_root") == scope:
            eligible_records.append((str(item.get("captured_at", "")), path, item))

    # Repeated hook deliveries are coalesced here, off the prompt-submit path.
    seen_turns: set[tuple[str, str, str]] = set()
    records = []
    for _, path, item in sorted(eligible_records, key=lambda entry: entry[0]):
        session_id = item.get("session_id")
        turn_id = item.get("turn_id")
        project = item.get("project_root")
        if isinstance(session_id, str) and isinstance(turn_id, str) and isinstance(project, str):
            key = (project, session_id, turn_id)
            if key in seen_turns:
                try:
                    path.unlink()
                except OSError:
                    continue
                continue
            seen_turns.add(key)
        records.append({"event_id": item["event_id"], "captured_at": item.get("captured_at"), "project_root": project})
    print(json.dumps(records, ensure_ascii=False))


def finish(args: argparse.Namespace) -> None:
    validate_event_id(args.event_id)
    config = settings()
    require_record_access(config)
    root = data_root()
    pending_path = root / "pending" / f"{args.event_id}.json"
    record = read_json(pending_path)
    if not record or record.get("event_id") != args.event_id:
        raise RuntimeError("Pending event not found or invalid.")
    require_record_access(config, record)
    if args.classification == "complaint":
        result = json.load(sys.stdin)
        if not isinstance(result, dict):
            raise RuntimeError("Expected a JSON object on stdin.")
        for key in ("prompt_summary", "assistant_mistake", "recommendation_report"):
            if not isinstance(result.get(key), str) or not result[key].strip():
                raise RuntimeError(f"Missing required field: {key}")
        # Explicit allowlist: never copy prompt, transcript, or session metadata.
        case = {
            "event_id": record["event_id"],
            "project_root": record.get("project_root"),
            "captured_at": record.get("captured_at"),
            "processed_at": timestamp(),
            "prompt_summary": result["prompt_summary"],
            "assistant_mistake": result["assistant_mistake"],
            "recommendation_report": result["recommendation_report"],
        }
        cases_dir = root / "cases"
        cases_dir.mkdir(parents=True, exist_ok=True)
        case_path = cases_dir / f"{args.event_id}.json"
        if not case_path.exists():
            atomic_json(case_path, case)
    # A result is durable before its original prompt/transcript path is removed.
    pending_path.unlink(missing_ok=True)
    print(json.dumps({"event_id": args.event_id, "classification": args.classification, "saved": args.classification == "complaint"}))


def configure(args: argparse.Namespace) -> None:
    root = data_root()
    value: dict[str, Any] = {"enabled": True, "scope": args.scope, "updated_at": timestamp()}
    if args.scope == "project":
        value["project_root"] = project_root()
    atomic_json(root / "settings.json", value)
    print(json.dumps({"enabled": True, "scope": args.scope, "project_root": value.get("project_root")}))


def disable(_: argparse.Namespace) -> None:
    config = settings() or {}
    config.update({"enabled": False, "updated_at": timestamp()})
    atomic_json(data_root() / "settings.json", config)
    print('{"enabled": false}')


def clear(_: argparse.Namespace) -> None:
    root = data_root()
    removed = 0
    for directory in (root / "pending", root / "cases"):
        if directory.exists():
            for path in directory.iterdir():
                if path.is_file():
                    path.unlink()
                    removed += 1
    print(json.dumps({"deleted_files": removed}))


def expire(_: argparse.Namespace) -> None:
    removed = expire_pending(data_root())
    print(json.dumps({"expired_files": removed}))


def session_start(_: argparse.Namespace) -> None:
    expire_pending(data_root())
    plugin_root = os.environ.get("PLUGIN_ROOT") or os.environ.get("CLAUDE_PLUGIN_ROOT")
    if not plugin_root:
        plugin_root = str(Path(__file__).resolve().parents[3])
    helper = Path(plugin_root) / "skills" / "angry-insight" / "scripts" / "queue.py"
    context = (
        "Angry Insight helper path: " + str(helper) + "\n"
        "Angry Insight data directory: " + str(data_root().resolve())
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }, ensure_ascii=False))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", help="PLUGIN_DATA directory supplied by the SessionStart hook.")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("capture")
    commands.add_parser("list")
    inspect_parser = commands.add_parser("inspect")
    inspect_parser.add_argument("event_id")
    finish_parser = commands.add_parser("finish")
    finish_parser.add_argument("event_id")
    finish_parser.add_argument("classification", choices=("complaint", "not-complaint"))
    config_parser = commands.add_parser("configure")
    config_parser.add_argument("--scope", choices=("project", "global"), required=True)
    commands.add_parser("disable")
    commands.add_parser("clear")
    commands.add_parser("expire")
    commands.add_parser("session-start")
    args = parser.parse_args()
    try:
        if args.data_dir:
            data_dir = Path(args.data_dir).expanduser()
            if not data_dir.is_absolute():
                raise RuntimeError("--data-dir must be an absolute path.")
            os.environ["PLUGIN_DATA"] = str(data_dir)
        if args.command == "capture":
            capture()
        elif args.command == "list":
            list_pending()
        elif args.command == "inspect":
            inspect(args.event_id)
        elif args.command == "finish":
            finish(args)
        elif args.command == "configure":
            configure(args)
        elif args.command == "disable":
            disable(args)
        elif args.command == "clear":
            clear(args)
        elif args.command == "expire":
            expire(args)
        elif args.command == "session-start":
            session_start(args)
        return 0
    except Exception as exc:
        print(f"angry-insight: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
