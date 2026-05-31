# Troubleshooting

## `bb-browser` command not found

Install it:

```bash
npm install -g bb-browser
```

Then verify:

```bash
command -v bb-browser
bb-browser --version
```

## Daemon not running

Check:

```bash
bb-browser daemon status --json
```

If the daemon is not running, a real command such as `open` may start it automatically:

```bash
bb-browser open "https://example.com" --json
```

If that still fails with `No page target found`, bootstrap a current tab first:

```bash
bb-browser tab new "https://example.com" --json
```

## Chrome CDP not reachable

Symptoms:

- daemon starts but cannot connect
- browser commands fail immediately

Checks:

```bash
bb-browser daemon status --json
```

If needed, make sure a Chromium-based browser is installed and available.

## No browser found

`bb-browser` expects a Chromium-family browser for CDP-backed control.

On macOS, common supported apps include:

- Google Chrome
- Microsoft Edge
- Brave

## `site` command missing or unknown

Refresh community adapters:

```bash
bb-browser site update
bb-browser site list
```

Then search again:

```bash
bb-browser site search "keyword"
```

## Snapshot refs are stale

If `click @3` or `fill @3` fails:

1. run a fresh snapshot
2. use refs from the new output only

```bash
bb-browser snapshot -i
```

Stale refs are normal after page changes.

## `No page target found`

This usually means the daemon is up but there is no current page target yet.

Reliable bootstrap sequence:

```bash
bb-browser tab new "https://example.com" --json
bb-browser wait 1500 --tab <tab> --json
bb-browser get title --tab <tab> --json
```

Once a current tab exists, `open`, `snapshot`, and `site` commands usually behave normally again.

## A task feels too click-heavy

Check whether one of these is faster:

```bash
bb-browser fetch "URL" --json
bb-browser network requests --with-body --json
bb-browser site search "keyword"
```

If a direct data path exists, prefer it over repeated UI interaction.
