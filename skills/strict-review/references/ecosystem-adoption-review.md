# Ecosystem and Adoption Review

Use this rubric when a change introduces or begins using a framework, library, plugin, adapter, or framework-specific configuration. Review broadly and shallowly; this is an ecosystem compatibility sweep, not a deep package audit.

## Activation signals

Activate when the change includes one or more of:

- a new direct dependency or framework import;
- a new plugin, adapter, preset, or framework configuration;
- a lockfile or package-manager change associated with a new capability;
- entry into a framework-specific runtime boundary;
- a version or build/test/lint integration change.

If classification is uncertain, activate the reviewer and record the uncertainty.

## Wide ecosystem sweep

Inspect the changed framework or library together with its nearby ecosystem:

- peer dependencies and companion packages;
- official adapters, plugins, and presets;
- TypeScript, bundler, test, and lint integration;
- browser/server/SSR/edge/runtime constraints;
- version compatibility visible in manifests and current official metadata;
- conventional integrations and existing project abstractions;
- deprecated, replaced, or incompatible usage patterns;
- capabilities the framework already provides that the change reimplements.

Use official documentation, package metadata, repository evidence, and trusted ecosystem sources when available. Do not claim exhaustive ecosystem coverage when external lookup was unavailable.

## Scope boundary

Do not deeply inspect package internals, perform a full supply-chain audit, or run installation/build/test commands in this reviewer. Those are separate concerns. Report only broad adoption or compatibility candidates, and let the core reviewers promote a candidate when concrete code evidence establishes a defect.

## Candidate record

Return records shaped like:

```yaml
ecosystem_candidate:
  change: new framework or library usage
  scope: package/config/runtime boundary
  observation: companion adapter or peer dependency may be required
  evidence:
    - changed manifest and import
    - current official integration guidance
  confidence: medium
  follow_up: confirm the project's runtime and configuration path
```

Keep the sweep wide enough to catch missing surrounding pieces, but shallow enough that it does not become an architecture essay. Separate confirmed code defects from ecosystem candidates.
