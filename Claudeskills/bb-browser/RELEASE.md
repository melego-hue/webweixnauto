# Release Notes Preparation

This repository is documentation-first, so a release is mostly about verifying examples and polishing GitHub presentation.

## Pre-release checklist

- Verify the repository name is `bb-browser-skill`
- Set the repository description to something close to:
  - `A cross-agent skill for using bb-browser with real browser login state`
- Suggested GitHub topics:
  - `bb-browser`
  - `ai-agents`
  - `codex`
  - `claude-code`
  - `cursor`
  - `mcp`
  - `browser-automation`
  - `chrome-devtools-protocol`
- Upload `assets/social-preview.png` as the GitHub social preview image

## Functional verification

Run:

```bash
command -v bb-browser
bb-browser --version
bb-browser daemon status --json
bb-browser site wikipedia/summary "Python (programming language)" --json
```

Then verify the tab bootstrap flow:

```bash
bb-browser tab new "https://example.com" --json
bb-browser wait 1500 --tab <tab> --json
bb-browser get title --tab <tab> --json
bb-browser snapshot -i --tab <tab> --json
```

## Release hygiene

- Move finished notes from `Unreleased` in `CHANGELOG.md` into a versioned section
- Re-read `README.md` for stale claims
- Ensure `SKILL.md` and `README.md` describe the same workflow
- Make sure every file path and command in the docs is copyable

## First public release suggestion

- Tag: `v0.1.0`
- Focus message:
  - public skill packaging
  - cross-agent install docs
  - verified `bb-browser` workflows
  - MCP integration guidance
