---
name: angry-insight
description: Analyze newly collected prompts for dissatisfaction with Codex responses and research ways to prevent confirmed mistakes from recurring.
---

# Angry Insight

Analyze only prompts newly collected in the project where Codex is running. The trusted `UserPromptSubmit` hook stores each prompt in a project-scoped local queue. The hook does not call a model or connect to an external service.

The trusted `SessionStart` hook provides the helper's absolute path and the plugin data directory in the session context, and performs expiration cleanup and migration of older queue entries. Use the provided paths for every command. For example: `python3 "<helper path>" --data-dir "<data directory>" list`. Hook processes receive `PLUGIN_ROOT` and `PLUGIN_DATA`, but ordinary shell commands may not. If the paths are missing from context, ask the user to review and trust the plugin hooks in `/hooks`, then start a new Codex session. Do not create queues or case files outside the provided data directory.

Entries from earlier versions are moved into the new project-scoped directory at session start or when the queue is listed. The old `settings.json` no longer controls whether prompts are collected.

## Hook Trust and Data Deletion

- When the user reviews and trusts the `UserPromptSubmit` hook in `/hooks`, collection begins with the next prompt. Ask them to review and trust the `SessionStart` hook as well, since it provides paths needed by the skill and performs expiration cleanup. No separate activation command or collection settings file is needed.
- To stop collection, the user can disable or untrust the hook in `/hooks`. Existing queued prompts and reports remain.
- If the user asks to delete Angry Insight data, run `python3 "<helper path>" --data-dir "<data directory>" clear`. This deletes queued prompts and saved cases for all projects. If the hooks remain trusted, future prompts will still be collected. This does not delete Codex conversation history files.
- Do not stop or change collection just because the user runs `$angry-insight` or asks about the feature.

## Analyze Pending Prompts

1. Run `python3 "<helper path>" --data-dir "<data directory>" list`. This expires queued records older than 30 days, merges duplicate events delivered for the same session and turn, and returns records for the current project only. If the result is empty, tell the user there are no new prompts to analyze.
2. For every returned `event_id`, run `python3 "<helper path>" --data-dir "<data directory>" inspect <event_id>`. Run independent `inspect` calls in parallel where possible to prepare records for analysis sub-agents. The command returns the prompt, project root, collection time, and the preceding Codex response when found in the conversation history. If no response is found, treat it as unknown and do not infer its contents. Conversation-history formats are not a stable interface; parsing failures must not delete queued records.
3. Divide the pending records into independently analyzable batches and assign one analysis sub-agent to each batch. Similar records may be grouped when there are many, but assign each `event_id` to exactly one agent. Start as many batches as available concurrent agent slots allow, then start the remaining batches as slots become available. Do not impose a fixed agent-count cap. Do not allow sub-agents to spawn more agents; the main skill agent owns assignment and synthesis. If sub-agents are unavailable, analyze the records directly. For every assigned event, each agent returns `complaint` or `not-complaint`, its reasoning, the confirmed response mistake, and the root cause. Do not perform generic sentiment analysis. Allow some false positives to reduce missed complaints. Profanity and exclamations are clues, but are not sufficient by themselves. Quoted language or profanity directed at someone else does not by itself indicate a complaint. Do not label a prompt `complaint` unless dissatisfaction with the preceding Codex response is clear; if the surrounding context cannot be checked, do not assume it.
4. Reconcile agent results by event and directly review any missing or conflicting classifications. For each `not-complaint`, run `python3 "<helper path>" --data-dir "<data directory>" finish <event_id> not-complaint`. Do not retain its prompt or create a report.
5. For each `complaint`, assign the anonymized summary and confirmed mistake to one solution-research sub-agent. That agent handles the full solution research for the assigned case and returns applicable solutions, limitations, and reference links. Do not split one case across multiple agents by research topic, and do not allow nested agent spawning. When there are multiple complaint cases, create an independent research task for each case, start as many as available concurrent agent slots allow, and queue the rest until slots become available. Do not impose a fixed agent-count cap. Assign each case to exactly one research agent; the main skill agent coordinates the work and reviews the results. If sub-agents are unavailable, research the cases directly. Give each agent only the anonymized summary and confirmed mistake, never the original prompt or conversation history. Relevant sources may include official Codex and Anthropic materials, Hacker News discussions, GitHub repositories, issues and pull requests, and npm packages or CLIs. The assigned agent chooses sources relevant to the case and returns actionable solutions, application guidance, limitations, and reference links—not a source-by-source list.

   Use only a brief anonymized case summary in search queries. Remove people, repositories, employers, and other identifying details. Do not put original prompts or conversation history in search queries, URLs, or reports. Sources are research routes, not report sections. Do not force irrelevant searches or invent results. Check maintenance status, license, and compatibility before recommending an npm package or CLI.
6. Review each research result by event. Check how each solution prevents the mistake in its assigned case, whether it fits the situation, and how it can be applied and what limitations it has. Attach reference links to the relevant solution. Do not merge findings from unrelated cases or report source-by-source summaries or irrelevant search results. Clearly label a proposal as an AI-generated idea when no applicable existing solution was found.
7. Combine the recommendation and its ready-to-apply artifact into one `권고 및 적용안` section. For a guidance-file change, name the target file and insertion point, and provide complete text to add. For code or configuration, provide the target path and an applicable diff or configuration example. For a process change, give the steps the user can follow. Read files in the current project only when needed to tailor the recommendation, and read them without modifying them. If a path or project structure cannot be confirmed, state the assumption and provide an adaptable draft. Do not modify user settings, instructions, code, or dependencies.
8. Save only complaint cases using this structure:

   ```json
   {
     "prompt_summary": "A short summary with identifying information removed",
     "assistant_mistake": "The confirmed mistake in the preceding response",
     "recommendation_report": "Solutions and limitations, recommendation and ready-to-apply artifact, reference links"
   }
   ```

   Pass this JSON to `python3 "<helper path>" --data-dir "<data directory>" finish <event_id> complaint`. The helper atomically saves the case before deleting the original prompt and conversation-history path. Do not include the original prompt, conversation-history contents or path, session ID, or turn ID in the JSON.
9. If classification, research, or case creation fails, do not run `finish`. Leave the record queued for retry until it expires after 30 days. Report the failure without exposing the original prompt.
10. Report only complaint cases analyzed in this run. Do not list older case files, re-evaluate past classifications, or infer recurring patterns. If there are no complaint cases, say so.

## Report Format

Write the user-facing report in Korean. Give each new complaint its own `##` heading, followed by the Korean headings `### 무슨 일이 있었나`, `### 가능한 해결책`, `### 권고 및 적용안`, and `### 적용 범위와 한계`. Use a separate `##` heading for each case when one run finds multiple cases.

- Show the classification as `complaint` below each case title.
- Under `무슨 일이 있었나`, combine the anonymized complaint summary, confirmed response mistake, and root cause. Do not repeat the root cause in the solutions or recommendation.
- Under `가능한 해결책`, describe only materially different alternatives and their tradeoffs. Do not list an immediate procedure as a duplicate solution.
- Under `권고 및 적용안`, explain why the recommendation fits and include the exact target path and insertion point, plus ready-to-apply text, a diff, configuration, or procedure.
- Under `적용 범위와 한계`, describe relevant constraints and say whether the proposal is an existing solution or an AI-generated idea.

Attach reference links to the relevant solutions. Do not create a source-by-source summary list.

Clearly disclose when conversation context could not be checked. Do not report or retain the contents of prompts classified as `not-complaint`.

## Model Input and External Services

To classify a follow-up message and summarize a confirmed mistake, the original prompt and preceding Codex response are included in the current Codex model's context. The user explicitly authorized this analysis input. Hooks themselves do not call a model or network. Never send original prompts or conversation-history contents to web search, external APIs, or remote databases. Use only anonymized summaries for research and store only anonymized content in saved reports.
