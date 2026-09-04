---
id: EU-ytxh
status: closed
deps: []
links: []
created: 2026-09-04T00:10:34Z
type: bug
priority: 2
assignee: ProbabilityEngineer
tags: [macos, menu, updates, edhm]
---
# Restore complete macOS menu and check EDHM mod updates

Fix native macOS menu labels and omitted File/View/Help menus, and change the update checker from EDHM-UI application releases to the current EDHM mod payload published in psychicEgg/EDHM/Odyssey.

## Acceptance Criteria

Settings… visibly appears in app menu; File, Edit, View, Window, Help menus are present with standard roles; dropdown says Check for EDHM Updates; checker queries EDHM payload version and compares it with installed EDHM version; arm64 package passes.

