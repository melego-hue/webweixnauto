# bb-browser CLI workflows

This reference expands the command-level workflow used by the main skill.

## 1. Preflight

Always start here:

```bash
command -v bb-browser
bb-browser --version
bb-browser daemon status --json
```

If the daemon is not running yet, a first real command such as `open` may launch the managed browser automatically.

## 2. Site-first workflow

For research, lookup, and data retrieval, check adapters before opening pages manually.

```bash
bb-browser site list
bb-browser site search "github"
bb-browser site info "github/search"
```

Typical calls:

```bash
bb-browser site zhihu/hot
bb-browser site github/search "model context protocol"
bb-browser site wikipedia/summary "Python (programming language)" --json
```

Use `--json` whenever the caller is another tool or agent.

## 3. Minimal page-control loop

When no adapter exists:

```bash
bb-browser tab new "https://example.com" --json
bb-browser wait 1500 --tab <tab> --json
bb-browser snapshot -i --tab <tab>
bb-browser get title --tab <tab>
```

Here `<tab>` is the short tab id returned in the `tab` field from `tab new`.

Why the extra bootstrap:

- some current `bb-browser` versions expect a current page target before `open`
- `tab new` creates that target
- `wait` gives the page time to settle before reading from it
- `snapshot --tab <tab>` and `get --tab <tab>` work reliably against that returned tab id

Then continue with refs from the latest snapshot:

```bash
bb-browser click @0
bb-browser fill @3 "hello"
bb-browser press Enter
bb-browser screenshot
```

## 4. Read-first inspection tools

Prefer these when possible:

```bash
bb-browser get url
bb-browser get title
bb-browser fetch "https://example.com/api" --json
bb-browser network requests --with-body --json
bb-browser console
bb-browser errors
```

These usually provide a cleaner path than repeatedly clicking through the page.

## 5. Snapshot rules

Snapshot again after:

- navigation
- clicking something that changes the page substantially
- opening or closing a modal
- changing tabs
- getting a stale or missing ref error

Refs are only trustworthy against the latest snapshot.

## 6. Clean-state bootstrap

If a fresh session reports:

```text
No page target found
```

use:

```bash
bb-browser tab new "https://example.com" --json
```

Then use the returned `tab` value:

```bash
bb-browser wait 1500 --tab <tab> --json
bb-browser get title --tab <tab> --json
bb-browser snapshot -i --tab <tab> --json
```

## 7. Recommended response strategy

When using `bb-browser` for a user task:

1. Say which command you ran
2. Prefer structured output over raw terminal noise
3. If a `site` command was available, mention that it was the preferred path
4. If you had to fall back to manual page control, say why
