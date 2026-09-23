# Angry Insight

`$angry-insight` reviews prompts that you explicitly opt in to store locally. It
looks for follow-up messages that express dissatisfaction with the immediately
preceding Codex response, then suggests ways to avoid the observed mistake.

## Opt in and trust the hook

Collection is off by default. Ask Codex to enable Angry Insight for the current
project or globally, for example:

```text
$angry-insight 이 프로젝트에서 수집을 켜줘
$angry-insight 전역으로 수집을 켜줘
```

Then inspect and trust the plugin's `UserPromptSubmit` hook in Codex's `/hooks`
screen. The hook stores prompts only after both the scope setting is enabled and
the hook is trusted. It makes no model or network calls.

The `SessionStart` hook provides the helper path and writable data directory to
the skill's context. Skill commands pass that data directory with `--data-dir`;
they do not assume hook-only environment variables are present in the shell.

Project scope records prompts only from the configured Git root (or the
configured directory when it is not a Git repository). Global scope records
prompts from any project. The hook stores them under the plugin's writable
`PLUGIN_DATA` directory. The helper checks that collection is enabled before
reading or finishing an event, and checks a project's event root in project
scope.

## Analyze and retain data

Run `$angry-insight` to analyze new pending prompts in the current scope. The
skill reads each prompt with the best available preceding assistant response
from its transcript, classifies it as `불만` or `불만 아님`, and searches Codex,
Anthropic, Hacker News, and npm for possible solutions to each complaint.
Search queries use only an anonymized complaint summary. Prompt and transcript
text are not sent to those search sources.

Pending prompt text and transcript paths remain local for up to 30 days of
active Codex use. The hook deletes expired entries on session start and
analysis; expired entries are never analyzed. With no Codex
process running, a local hook cannot execute at the exact expiration time.
After successful analysis,
non-complaint entries are deleted. For a complaint, the helper atomically saves
an anonymized summary, observed mistake, and recommendation report before
deleting the raw prompt and transcript path. Transcript files themselves are
never deleted. A failed analysis leaves the pending entry available for retry
until it expires. Saved complaint reports remain in `PLUGIN_DATA/cases/` until
you clear them or remove the plugin data directory.

Prompt submission writes one event file without scanning the queue. Expiration
cleanup runs at session start and when the skill lists pending events. Duplicate
session/turn deliveries are coalesced when the skill lists pending events.

If the transcript cannot be parsed or the preceding response is unavailable,
the skill reports that limitation and avoids guessing. Transcript formats are
not a stable Codex hook interface.

## Manage collection and local data

Ask Codex to stop collection to disable future capture; this preserves pending
prompts and reports. Ask to erase Angry Insight data to remove pending prompts
and saved reports. The original Codex transcript files remain untouched.

## Privacy and changes

The plugin stores data only under its writable `PLUGIN_DATA` directory. It does
not send prompts or transcripts to web search, external APIs, or remote
databases. However, when `$angry-insight` runs, it includes the prompt and the
best-effort preceding response in the current Codex model's context so the model
can classify and summarize the case. The hook itself makes no model or network
calls. Web research uses only an anonymized case summary and returns source
links in the locally saved report.

The plugin does not install packages or modify settings, instructions, or code.
