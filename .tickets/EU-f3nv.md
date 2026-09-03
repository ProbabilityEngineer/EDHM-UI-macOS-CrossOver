---
id: EU-f3nv
status: closed
deps: []
links: []
created: 2026-09-03T23:56:11Z
type: feature
priority: 2
assignee: ProbabilityEngineer
tags: [ui, menu, edhm, status]
---
# Hide redundant EDHM install menu action

Dynamically show only Install EDHM or Un-install EDHM in the renderer dropdown based on the active game's EDHM installation state. Preserve both actions while status is still unknown.

## Acceptance Criteria

Installed or disabled EDHM shows Un-install EDHM but not Install EDHM; not-installed state shows Install EDHM but not Un-install EDHM; unknown state remains safe and does not hide both actions; state refreshes after install, uninstall, and instance changes.

