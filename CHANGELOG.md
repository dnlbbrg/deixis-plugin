# Changelog

All notable changes to this plugin are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-10-21

### Added

- Plugin marketplace `deixis` with the plugin `deixis`, installable with `claude plugin marketplace add dnlbbrg/deixis-plugin`.
- MCP server `deixis`, started through the launcher `bin/deixis-mcp`, which runs the MCP helper that ships inside Deixis.app. Tools: `list_rounds`, `get_round`, `get_point`, `get_round_overview`, `watch_rounds`, `reply` and `set_status`.
- The launcher looks for Deixis.app in `/Applications`, then `~/Applications`, then through Spotlight. Outside `/Applications` it only runs a copy that is validly signed by the Deixis developer team.
- Command `/deixis-watch`, which waits for feedback rounds and works through each one as it arrives.
- Session hooks `SessionStart`, `UserPromptSubmit` and `SessionEnd`. They exit quietly when Deixis.app is not installed.

[Unreleased]: https://github.com/dnlbbrg/deixis-plugin/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/dnlbbrg/deixis-plugin/releases/tag/v0.1.0
