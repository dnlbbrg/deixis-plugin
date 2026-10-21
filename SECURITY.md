# Security

## Reporting a vulnerability

Please report security issues privately by email to [post@danielboberg.de](mailto:post@danielboberg.de). Do not open a public issue for them.

Include what you found, the steps to reproduce it, and the versions of the plugin, Deixis and macOS you used. You will get a reply by email. Once a fix is released, you can be credited in the changelog if you like.

## Scope

This repository contains the Claude Code plugin, not the Deixis app. In scope are:

- The launcher script `plugin/bin/deixis-mcp`: how it finds Deixis.app and which binary it executes.
- The session hooks in `plugin/hooks/hooks.json` and the command `/deixis-watch`.
- The plugin and marketplace configuration in `plugin/.claude-plugin/`, `plugin/.mcp.json` and `.claude-plugin/`.

The launcher runs the helper from `/Applications/Deixis.app` directly. A copy anywhere else (`~/Applications` or a location found through Spotlight) only runs if `codesign` verifies it and its Team Identifier matches the Deixis developer team. A way to make the launcher run a binary that does not pass this check is in scope.

Issues in the Deixis app itself are also welcome at the same address, though the app is not part of this repository.
