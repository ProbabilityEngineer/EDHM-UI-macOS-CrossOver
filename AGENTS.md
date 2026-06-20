# AGENTS.md

## Scope

These instructions apply to the entire `EDHM_UI` repo.

## Project focus

- Prioritize the Electron/Vue app in `source_v3/` for current macOS work.
- Current macOS proof-of-concept targets native app packaging plus manual CrossOver bottle paths.
- Prefer minimal, working mac fixes over broad architecture cleanup unless the user asks for a refactor.

## Workflow

- Start with the most specific code-intelligence tool available.
- Use explicit repo-relative paths in reads, searches, and edits.
- For syntax-shaped requests, prefer AST/LSP before broad text search.
- For behavior or intent requests, prefer semantic/code-intelligence search before file listing.
- Use diagnostics before broad builds when an LSP is available.

## Structural edits

- Prefer ast-grep for simple structural replacements.
- Use precise text edits for complex multi-line changes.

## Tickets

- Use tk tickets for non-trivial feature, fix, packaging, or workflow work.
- Continue using the existing repo ticket flow under `.tickets/`.
- Ticket actions may modify `.tickets/` but should not touch code unless the task requires it.

## Turnlog

- Record meaningful repo work in turnlog, especially code changes, packaging/debugging, ticket updates, and workflow setup.
- Keep `.turnlog/` out of GitHub unless this repo explicitly chooses to track it.

## Jujutsu and Git

- Use `jj` for local VCS work: `jj status`, `jj diff`, `jj log`, `jj describe -m "message"`, `jj new --no-edit`, `jj op log`, and `jj undo`.
- Use Git only for remote interoperability.
- Do not use staged-index workflows like `git add`, `git commit`, `git diff --cached`, or `git pull --rebase`.
- Before starting work, inspect `jj status`.
- After a coherent agent-owned change, run `jj describe -m "message"` and `jj new --no-edit`.
- Prefer `/jj-align-push [branch]` for final alignment/publishing when requested.

## Shell

- Prefer explicit paths for file operations.
- Avoid interactive prompts in automation.
- Ask before deleting files or directories.
- Set `HOMEBREW_NO_AUTO_UPDATE=1` for Homebrew commands.

## macOS / CrossOver guidance

- Use mac-standard app data at `~/Library/Application Support/EDHM-UI-V3`.
- Use cache/temp at `~/Library/Caches/EDHM-UI-V3`.
- Treat these as separate user inputs when relevant:
  - game install folder
  - Player Journal folder
  - Elite config XML folder
- The XML folder is the folder containing `GraphicsConfiguration.xml` and/or `GraphicsConfigurationOverride.xml`.
- CrossOver bottles come first; generic Wine support can follow later.

## Packaging

- For `source_v3`, prefer Node 22 for Forge package work.
- On macOS, prefer rebuilding the app over patching packaged `app.asar` files directly.
