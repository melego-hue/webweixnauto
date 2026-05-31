# Example prompts

These examples are written so they can be adapted for Codex, Claude Code, Cursor, or other agent runtimes.

## Site-first

```text
Use $bb-browser to search GitHub for "model context protocol" and summarize the top results. Prefer a site command if one exists.
```

```text
Use $bb-browser to read the current Zhihu hot list and return the top 10 entries in structured form.
```

## Manual page workflow

```text
Use $bb-browser to open example.com, inspect the interactive elements, and tell me the page title plus the main link target.
```

```text
Use $bb-browser to open a page, snapshot it, and explain which element refs are relevant before clicking anything.
```

## MCP setup

```text
Use $bb-browser to show me the MCP configuration needed to connect bb-browser to my agent runtime, then list the first three verification commands I should run.
```

## Safety-sensitive

```text
Use $bb-browser to inspect the logged-in page and tell me what actions would have side effects. Do not perform any write action without explicit confirmation.
```
