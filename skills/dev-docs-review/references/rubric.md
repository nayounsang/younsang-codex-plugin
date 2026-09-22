# Developer documentation review rubric

Apply this rubric after checking the documented claims against the project context dossier. Report only dimensions with evidence and a user consequence.

## Technical accuracy

Check imports, exported names, signatures, types, schemas, command names, positional arguments, flags, configuration keys, defaults, supported features, version ranges, error behavior, lifecycle/cleanup, URLs, identifiers, and stated limitations. A claim that cannot be checked in code, tests, execution, or an authoritative external source is **unverified**, not automatically wrong.

## Executability and task completion

Trace installation or setup to first success. A runnable example identifies prerequisites, working directory, environment, exact command or code, expected output, and cleanup/reset. Check normal flow, common failure, recovery, and the next step. Compare examples across pages for compatible versions, flags, IDs, configuration, and state.

## Information architecture and discoverability

Classify each page as tutorial, how-to, reference, explanation, migration note, or overview. Check titles, headings, links, navigation, redirects, version selectors, hidden pages, and next steps. A reader should be able to find the task, understand the prerequisite, complete it, and continue without competing canonical versions.

## Relevance and information density

Flag boilerplate, repeated prose, stale scaffold text, unrelated implementation detail, and content that does not support the reader's decision. Put the task, outcome, prerequisites, and important warning early. Keep one dominant purpose per page; move deep reference detail to a linked reference when it interrupts a task.

## Terminology

Prefer ordinary words when they preserve meaning. Preserve established ecosystem terms, public symbols, commands, protocols, and UI labels when they are the contract. Check first-use definitions, one name per concept, distinct names for distinct concepts, casing, pluralization, and overloaded terms. Require evidence for a terminology finding: public code/type/CLI/UI, a recognized standard, authoritative ecosystem usage, or an explicit project definition.

## Clarity and readability

Prefer direct sentences, concrete subjects, active voice, defined abbreviations, and unambiguous references. Use lists for parallel items, tables for meaningful comparisons, tabs or separate sections for environment alternatives, and callouts for prerequisites or warnings when those structures materially improve scanning. Do not flag style preferences without a concrete comprehension consequence.

## Consistency and drift

Compare product/module names, commands, casing, link labels, code/config fields, defaults, version claims, and behavior descriptions across overview pages, READMEs, tutorials, reference pages, and generated output. Identify a canonical source and recommend a summary/link elsewhere when the same specification is duplicated. Distinguish current implementation from roadmap or future language.

## Freshness and version clarity

Check dependency and runtime support, peer/version ranges, deprecated interfaces, migration paths, release selectors, and date-sensitive claims. Do not infer that a roadmap promise is implemented. If the branch or build state is not representative of a published version, say so.

## Accessibility

Check descriptive link text, sequential headings, useful image alt text, readable code examples, table semantics, keyboard-relevant instructions, and whether required information is communicated only by color, position, animation, or an image.

## Safety and operations

For remote debugging, destructive commands, file deletion, unbounded repetition, external calls, credential use, production data, or other mutations, require bounded scope, an explicit warning, isolated data/profile where appropriate, and a stop/reset/cleanup procedure. Check that examples do not silently target a user's regular environment or real data.

## Maintainability

Identify which docs must change when a public export, schema, command, UI label, configuration field, or generated page changes. Distinguish generated output from the maintained source and avoid recommending edits to generated artifacts. Prefer a single canonical contract with concise summaries and links elsewhere.

## External references

Use the authoritative documentation for the relevant language, framework, protocol, platform, or standard when repository evidence does not define an external contract. General writing references can include [Diátaxis](https://diataxis.fr/), the [Google developer documentation style guide](https://developers.google.com/style), and the [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/), but an external style guide is not evidence that a project-specific behavior is supported.
