---
id: EU-prjk
status: closed
deps: []
links: []
created: 2026-09-04T00:40:32Z
type: feature
priority: 2
assignee: ProbabilityEngineer
tags: [macos, wine, crossover, settings, ui]
---
# Simplify settings layout and clarify Wine override action

Remove the unnecessary Other Settings card nesting while preserving all contained controls. Rename the override action and related user-facing copy to Wine DLL Overrides, while retaining existing CrossOverBottlePath compatibility keys and IPC APIs.

## Acceptance Criteria

General Settings no longer displays an Other Settings heading/card; all existing journal, prefix/bottle, XML, theme count, and action controls remain usable; override button reads Configure Wine DLL Overrides; user-facing messages use Wine terminology; package validation passes.

