# AGENTS.md

## Scope

These instructions apply to the entire `EDHM_UI` repo.

## Project focus

- Prioritize the Electron/Vue app in `source_v3/` for current macOS work.
- Current macOS proof-of-concept targets native app packaging plus manual CrossOver bottle paths.
- Prefer minimal, working mac fixes over broad architecture cleanup unless the user asks for a refactor.
- Keep Windows behavior intact where practical; mac work should be additive unless replacing clearly broken assumptions.

## Working norms

- Start with the most specific code-intelligence tool available.
- Use explicit repo-relative paths in reads, searches, and edits.
- For syntax-shaped requests, prefer AST/LSP before broad text search.
- For behavior or intent requests, prefer semantic/code-intelligence search before file listing.
- Use diagnostics before broad builds when an LSP is available.
- Be careful not to mix the legacy `source/` app and the current `source_v3/` Electron app unless the task explicitly spans both.

## Structural edits

- Prefer ast-grep for simple structural replacements.
- Use precise text edits for complex multi-line changes.
- For packaged Electron output, edit source files first and rebuild rather than patching packaged artifacts directly.

## Tickets

- Use tk tickets for non-trivial feature, fix, packaging, or workflow work.
- Continue using the existing repo ticket flow under `.tickets/`.
- Ticket actions may modify `.tickets/` but should not touch code unless the task requires it.
- Keep ticket notes concise and outcome-focused: what changed, why, and what remains.

## Turnlog

- Record meaningful repo work in turnlog, especially code changes, packaging/debugging, ticket updates, VCS operations, and workflow setup.
- Before final VCS publication of a coherent change, record what changed, validation performed, and any ticket touched.
- Keep `.turnlog/` out of GitHub unless this repo explicitly chooses to track it.

## Jujutsu and Git

- Use `jj` for local VCS work: `jj status`, `jj diff`, `jj log`, `jj describe -m "message"`, `jj new --no-edit`, `jj op log`, and `jj undo`.
- Use Git only for remote interoperability.
- Do not use staged-index workflows like `git add`, `git commit`, `git diff --cached`, or `git pull --rebase`.
- Before starting work, inspect `jj status`.
- After a coherent agent-owned change, run `jj describe -m "message"` and `jj new --no-edit`.
- Keep `@` empty when a change is complete; the finished work should sit in `@-`.
- Use clear `jj describe` messages because they are part of the working record for this repo.
- Prefer `/jj-align-push [branch]` for final alignment/publishing when requested.

## Remote layout

- Treat this repo as a fork-style checkout.
- `upstream` should refer to the original BlueMystical repository.
- `origin` should refer to the user's fork when available.
- Avoid pushing directly to upstream unless the user explicitly asks for it.

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
- For UI work on macOS, watch for Retina scaling issues before changing component CSS.

## Packaging

- For `source_v3`, prefer Node 22 for Forge package work.
- When validating packaging changes, prefer a fresh `npm run package` over dev-only validation.
- If a packaged mac app behaves oddly, verify source settings/bootstrap logic before assuming packaging corruption.
