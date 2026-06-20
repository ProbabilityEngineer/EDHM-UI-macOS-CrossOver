---
id: EU-0ija
status: open
deps: []
links: []
created: 2026-06-20T05:37:54Z
type: epic
priority: 2
assignee: Samuel Collins
tags: [macos, electron, planning, refactor]
---
# Plan macOS-native refactor for EDHM_UI v3

Inspect EDHM_UI v3 Electron app, initialize tickets, and produce a phased plan to support native macOS builds and CrossOver/Wine Elite installs.


## Notes

**2026-06-20T06:08:57Z**

Initial macOS refactor review of source_v3 complete. Findings: (1) packaging is Windows-first in source_v3/forge.config.js with no active mac target; commented Linux config suggests intended multi-platform support. (2) Runtime already partially supports darwin/linux in Electron main process and FileHelper path resolution, but many defaults still hard-code Windows env vars (%USERPROFILE%, %LOCALAPPDATA%) and Windows install layout. (3) Game instance detection in SettingsHelper.addNewInstance() infers publisher from path substrings like steamapps/Epic Games/Frontier and maps by Windows-style install folder names. (4) Mod install/uninstall logic assumes Windows game process names and paths, creates symlinks with junction type, and uses Windows-specific hotfix/UI exe paths. (5) FileHelper has mixed platform coverage: openPathInExplorer supports darwin, terminateProgram supports non-Windows via pgrep/kill, but runInstaller supports only win32/linux and runScripOrProgram supports only win32/linux. Recommended phases: A) introduce platform services for app-data/temp/desktop/game-root paths and process launching; B) make forge config platform-aware and add mac packaging/assets; C) add CrossOver/Wine game-instance discovery/provider layer; D) remove Windows-only assumptions from install/hotfix/uninstall flows; E) validate native mac app against a CrossOver bottle.

**2026-06-20T06:24:48Z**

Implemented first macOS path pass in source_v3 as proof of concept. Added FileHelper helpers getAppDataRoot/getCacheRoot/getTempRoot and env vars %EDHM_APPDATA%/%EDHM_CACHEDATA%/%EDHM_TEMPDATA%. Moved program settings root to app-specific platform paths (mac: ~/Library/Application Support/EDHM-UI-V3, cache/temp under ~/Library/Caches/EDHM-UI-V3). Updated SettingsHelper, ThemeHelper, LoggingHelper, and default Settings.json to use the app-data root instead of hard-coded %USERPROFILE%\\EDHM_UI and %LOCALAPPDATA% temp paths. Left broader game-discovery/install abstraction for follow-up; current goal is minimal mac proof of concept.

**2026-06-20T06:31:21Z**

Added proof-of-concept manual path UX for mac/CrossOver in source_v3 SettingsEditor. New config field PlayerConfigFolder defaults to the Windows Elite graphics config folder path. Settings UI now exposes separate fields for Player Journal Location and Elite Config XML Folder, with browse actions and Windows default guidance text. Game executable browse flow now prompts for missing journal/config folders after manual executable selection, and the localization wizard messaging now explicitly mentions manual setup on mac/CrossOver. Also updated user-data relocation to write primary settings under %EDHM_APPDATA% rather than hard-coded %LOCALAPPDATA%\\EDHM-UI-V3. This is still a minimal PoC; PlayerConfigFolder is collected and persisted but not yet consumed by downstream XML-mod logic.

**2026-06-20T06:36:08Z**

Wired the new PlayerConfigFolder into XML file resolution at the FileHelper layer. Added getConfiguredGraphicsFolder() and resolveXmlFilePath() so read-xml-file/write-xml-file now redirect GraphicsConfiguration.xml and GraphicsConfigurationOverride.xml to the configured Elite graphics folder when callers pass a non-existent or bare path. This is a minimal PoC approach that avoids broader mod-data/path abstraction changes for now; follow-up could make XML-aware callers explicit rather than relying on helper-level redirection.

**2026-06-20T06:39:35Z**

Added minimal mac packaging support in source_v3/forge.config.js. Config is now platform-aware: Windows keeps the Squirrel maker and .ico icon, while mac uses a generated .icns asset and the generic zip maker. Generated a proof-of-concept mac icon at source_v3/src/images/EDHM-UI-V3.icns from the existing PNG art. Packaging is not fully validated yet because source_v3 dependencies are not installed in this environment (requiring forge plugins fails until npm install is run).

**2026-06-20T06:49:29Z**

Packaging follow-up: trimmed packager copy scope by adding packagerConfig.ignore for /out, /build, /.vite, and /.git in source_v3/forge.config.js. Rationale: package was hanging during Electron Packager 'Copying files'; these generated directories should not be copied into the app source payload because settings_window is already re-added explicitly through extraResource and build artifacts are transient. This is a pragmatic PoC packaging optimization, not a final packaging audit.

**2026-06-20T06:55:58Z**

Successfully built a packaged mac app after debugging packaging. Root cause was running the Electron Forge packaging stack under Node 26; packaging exited prematurely during/after Electron extraction with no output bundle. Re-running under Node 22 via `npx -y -p node@22 -c 'DEBUG=electron-forge:*,electron-packager npm run package'` completed successfully and produced `source_v3/out/EDHM-UI-V3-darwin-arm64/EDHM-UI-V3.app`. Also reverted the custom packager ignore override and let @electron-forge/plugin-vite supply its expected ignore function.

**2026-06-20T06:59:51Z**

Adjusted packaged app UI density for mac proof-of-concept without touching HUD graphics. In source_v3/src/index.css, reduced default --user-font-size from 14px to 12px, removed body max-width/padding, and tightened Bootstrap-derived button/nav/form control paddings via CSS variables. This should shrink oversized text and control chrome while leaving image/canvas HUD graphics unchanged.

**2026-06-20T07:21:37Z**

Adjusted mac UI scaling logic in source_v3/src/main.js. The app had been applying Electron zoomFactor equal to the macOS Retina display scaleFactor (e.g. 2x), which made the entire UI huge. Automatic scaling on darwin now defaults to zoomFactor 1 unless the user explicitly sets UiScaleFactor.

**2026-06-20T07:27:29Z**

Removed the non-useful blue/green toast guidance from the settings dialog on mac PoC. In source_v3/src/SettingsWindow/SettingsEditor.vue, the first-run info toast and game localization assistant info/success RoastMe notifications were removed so the settings UI opens cleanly without overlay boxes.

**2026-06-20T07:33:03Z**

Removed legacy Custom Icon UI/code from the in-app settings modal (src/MainWindow/SettingsEditor.vue) and stripped the non-useful green/blue RoastMe notifications from that modal's first-run and game localization assistant flow. This addresses the remaining popups the user was seeing in the packaged app.
