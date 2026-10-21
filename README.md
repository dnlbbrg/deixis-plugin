# Deixis plugin for Claude Code

Connects Claude Code to [Deixis](https://deixis.folnaro.app), the Mac app for screenshot feedback: point at
something on screen, say or type what should change, and the round arrives in the right session with its images.

```sh
claude plugin marketplace add dnlbbrg/deixis-plugin
claude plugin install deixis@deixis
```

The plugin starts the MCP helper that ships inside Deixis.app (Mac App Store). The helper runs locally over stdio and
makes no network connections; what Claude Code then sends to its provider is governed by Claude Code.
Other agents (Codex, Cursor, VS Code, Windsurf, Zed, JetBrains, Gemini CLI, Claude Desktop) are set up from
the app's settings.
