# MCP integration

This reference shows how to expose `bb-browser` as an MCP server for agent runtimes.

## General rule

Verify the CLI first:

```bash
bb-browser --version
bb-browser daemon status --json
```

Only then configure MCP.

## Base configuration

```json
{
  "mcpServers": {
    "bb-browser": {
      "command": "npx",
      "args": ["-y", "bb-browser", "--mcp"]
    }
  }
}
```

## Codex-style usage

Use the base configuration above in the runtime's MCP configuration file or UI.

Recommended pattern:

1. Confirm `bb-browser` works from the terminal
2. Add the MCP entry
3. Restart or reload the agent runtime
4. Test a simple flow first

Suggested first task:

- ask the agent to query a known `site` command
- then ask it to open a page and read the title

## Claude Code / Cursor style usage

Use the same base MCP entry if the runtime accepts command-based MCP servers.

If the product requires a JSON file, paste the `mcpServers` object into the relevant configuration.

## Validation sequence

After wiring MCP:

1. test a `site` query
2. test a page open
3. test a simple read operation such as `get title`

This narrows failures quickly:

- if `site` fails, the MCP bridge or CLI path may be wrong
- if `site` works but `open` fails, check browser/CDP readiness
- if `open` works but later refs fail, check your snapshot discipline
