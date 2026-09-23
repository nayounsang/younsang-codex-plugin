---
name: angry-insight
description: Analyze locally queued Codex prompts for complaints about the immediately preceding Codex response, then research and report practical recurrence prevention ideas. Use only when the user invokes $angry-insight or asks to configure this feature.
---

# Angry Insight

Analyze only newly pending prompts that fall within the enabled project or global scope. The hook only queues prompts locally; it does not call a model or any external service.

At session start, the plugin hook provides the helper's absolute path and the plugin's writable data directory as context. Use those exact paths in each CLI command, for example `python3 "<helper path>" --data-dir "<data directory>" list`. The hook process itself receives `PLUGIN_ROOT` and `PLUGIN_DATA`; regular shell commands may not. If the paths are missing from the context, ask the user to start a new Codex session after reviewing and trusting the hook. Do not create queue or case files outside the supplied data directory.

## Enable, disable, and clear

- Collection is off until the user explicitly opts in. When the user asks to enable or set up Angry Insight, ask whether to enable for this project or globally if they have not specified a scope, then run `python3 "<helper path>" --data-dir "<data directory>" configure --scope project` or `--scope global`.
- Project scope stores prompts only when the current Git root (or current directory outside Git) matches the configured root. Global scope stores prompts from every project. In either scope, reports are shown only for events selected for the current invocation.
- If the user asks to stop collection, run `python3 "<helper path>" --data-dir "<data directory>" disable`. This leaves existing pending prompts and reports in place.
- If the user asks to erase Angry Insight data, run `python3 "<helper path>" --data-dir "<data directory>" clear`. It removes pending prompts and saved cases; it does not remove Codex transcript files.
- Do not enable collection just because the user invokes `$angry-insight` to analyze or asks what the feature does. If disabled, explain how to opt in and stop without reading any queued data.

## Analyze pending prompts

1. Run `python3 "<helper path>" --data-dir "<data directory>" list`. This expires pending records older than 30 days, coalesces duplicate session/turn deliveries, and returns only records in the active scope. If empty, say there are no new prompts to analyze.
2. For each returned `event_id`, run `python3 "<helper path>" --data-dir "<data directory>" inspect <event_id>`. It outputs only that prompt, project root, capture time, and the best-effort preceding assistant response from the transcript. Treat a missing response as unavailable; never guess what Codex said. The transcript format is not a stable interface, so a parse failure is not a reason to discard the pending record.
3. Classify the user's follow-up strictly as one of `불만` or `불만 아님`, based on whether it signals dissatisfaction with the immediately preceding Codex response. Do not perform general sentiment analysis. Allow some false positives to avoid missing complaints. Swearing and exclamations are clues, not sufficient alone; quoted language or profanity aimed at someone else is not a complaint by itself. If context is unavailable, do not invent it; judge only clear dissatisfaction directed at Codex's prior answer.
4. For `불만 아님`, run `python3 "<helper path>" --data-dir "<data directory>" finish <event_id> not-complaint`. Do not retain its prompt or a report.
5. For `불만`, write a short, privacy-safe summary of the complaint, a short summary of the observed assistant mistake, and a recommendation report. Search all four required sources for each case:
   - Codex official docs, examples, plugins, and skills.
   - Anthropic official Claude Code features (including `/insight`), docs, examples, plugins, and skills.
   - Hacker News discussions about similar problems and user experience.
   - npm packages or CLIs. For any candidate you recommend, assess maintenance, license, and compatibility.

   Search only with the short case summary. Remove personal, repository, employer, and other identifying details from search terms. Never search using the prompt text or transcript, and never include either in a search query, URL, or report. Use live web search and cite direct links. If an access method is unavailable, report that source as not searched; do not claim to have searched it.
6. For each source, summarize the closest useful result or say that no suitable solution was found. Explain applicability, constraints, and a concrete recommendation. Clearly label a solution you devised as an AI-proposed idea when no suitable existing solution is available. Do not install dependencies or edit user settings, instructions, or code.
7. Save only the complaint result with:

   ```json
   {
     "prompt_summary": "Short, identifying details removed",
     "assistant_mistake": "Observed mistake in the preceding answer",
     "recommendation_report": "Source links, applicability, constraints, and recommendation"
   }
   ```

   Pipe this JSON to `python3 "<helper path>" --data-dir "<data directory>" finish <event_id> complaint`. The helper writes the case atomically before deleting the raw prompt and transcript path. Do not put prompt text, transcript text/path, session ID, or turn ID into the JSON.
8. If classification, research, or case creation fails, do not call `finish`; the item stays pending for retry until it reaches 30 days. Report failures without exposing raw prompt text.
9. Report only complaint cases analyzed during this invocation. Do not list old case files, revisit past classifications, or infer repeat patterns. If there were no complaints, say so.

## Output

For each new complaint, report:

- Complaint summary and observed assistant mistake.
- Findings from Codex, Anthropic, Hacker News, and npm, with links and applicability.
- Concrete recurrence prevention recommendation, constraints, and whether it is an existing solution or AI-proposed.

Clearly state when transcript context was unavailable. Never report a non-complaint prompt's text or retain it.

## Model input and external services

To classify the follow-up and summarize the observed mistake, the prompt text and the best-effort preceding Codex response are included in the current Codex model's context when this skill runs. The user has explicitly accepted this analysis input. The hook itself does not call a model or network service. Do not send raw prompt or transcript content to web search, external APIs, or remote databases; research queries and saved reports use only anonymized summaries.
