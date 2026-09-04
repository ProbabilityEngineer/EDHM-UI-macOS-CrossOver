---
id: EU-en06
status: closed
deps: []
links: []
created: 2026-09-04T01:09:02Z
type: task
priority: 1
assignee: ProbabilityEngineer
tags: [release, macos, notarization]
---
# Release EDHM-UI-Mac 3.1.0

Create the first independently versioned macOS release after upstream 3.0.70, update app/about version metadata, build arm64 and universal notarized ZIPs, publish GitHub release, and align/push the feature bookmark.

## Acceptance Criteria

Version is 3.1.0 in package metadata/about display; signed notarized arm64 and universal ZIPs are attached to GitHub release macos-crossover-v3.1.0; bookmark is aligned and pushed.


## Notes

**2026-09-04T01:13:16Z**

Version 3.1.0 committed and macos-crossover-poc pushed to origin. arm64 and universal signed packages built and verified. GitHub release/tag and notarization remain pending because no notarytool keychain profile or Apple API credentials are available.
