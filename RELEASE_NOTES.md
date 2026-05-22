# Release Notes

## v1.0.0 - macOS Community Release

Initial macOS community release of the Antigravity IDE migration utility.

### Highlights

- macOS path support for `~/Library/Application Support/Antigravity` to `~/Library/Application Support/Antigravity IDE`
- one-click `.command` launchers for dry-run, migration, restore, and cleanup
- automatic backup before real migration writes
- full migration-target restore for failed or unwanted migrations
- dry-run mode without backup side effects
- migration of settings, Local State, root app state, profile data, history, workspace storage, extensions, Gemini data, and SQLite state records
- macOS process checks for Antigravity and Antigravity IDE
- unit tests covering the key migration paths

### Positioning

This is the macOS companion to the original Windows-focused Antigravity IDE migration tool.

Published for the community courtesy of Equilibrium.com and CPUcoin.io.
