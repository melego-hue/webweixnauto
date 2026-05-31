# Contributing

Thanks for contributing to `bb-browser-skill`.

This repository is intentionally small: the goal is to keep the public skill easy to understand, easy to install, and honest about current `bb-browser` behavior.

## What belongs here

Good contributions include:

- clearer skill triggering and guardrails
- better cross-agent installation guidance
- stronger `bb-browser` workflow examples
- troubleshooting notes backed by real behavior
- UI metadata improvements for compatible runtimes

## What does not belong here

Please avoid using this repository for:

- new `bb-browser site` adapter development
- general Playwright or browser testing advice
- large unrelated prompt collections
- speculative features with no verified workflow

## Contribution principles

- Keep `SKILL.md` focused and lightweight
- Put deeper details in `references/`
- Prefer verified examples over idealized examples
- Document current behavior, including quirks, instead of hiding them
- Preserve cross-agent usefulness; do not overfit to one runtime unless clearly labeled

## Suggested workflow

1. Update `README.md` if the user-facing behavior changes
2. Update `SKILL.md` if invocation or workflow guidance changes
3. Update `references/` when adding deeper operational detail
4. Keep examples aligned with real commands that have been exercised

## Before opening a pull request

Please verify:

```bash
command -v bb-browser
bb-browser --version
bb-browser daemon status --json
```

And, when relevant:

```bash
bb-browser site wikipedia/summary "Python (programming language)" --json
bb-browser tab new "https://example.com" --json
```

If your change affects documented workflows, mention what you verified in the PR description.
