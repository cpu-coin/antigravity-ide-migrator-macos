# Antigravity IDE Migrator for macOS

Community macOS migration utility for moving legacy Antigravity data into Antigravity IDE.

Courtesy of Equilibrium.com and CPUcoin.io.

This repository is the macOS companion to the original Windows-focused Antigravity IDE migration tool by winteryu21:

```text
https://github.com/winteryu21/Damn-Antigravity-IDE-Migrator
```

It keeps the same safety-first migration model and adapts the paths, launchers, and profile-state handling needed for macOS.

## What It Migrates

The tool migrates local data from:

```text
~/Library/Application Support/Antigravity
~/.antigravity
~/.gemini/antigravity
```

to:

```text
~/Library/Application Support/Antigravity IDE
~/.antigravity-ide
~/.gemini/antigravity-ide
```

It copies or merges:

- user settings
- Local State safeStorage metadata
- global storage registry data
- profile state
- workspace state
- history files
- cached profile data
- root app storage
- extension folders and extension metadata
- Gemini data
- SQLite-backed conversation and state records

## Safety

Close both Antigravity and Antigravity IDE before running this tool.

The migration is local-only. It does not contact a remote service during migration. A real migration creates a timestamped backup before modifying destination files. Dry-run mode shows the planned work without writing migrated data.

Backups are full migration-target snapshots. Restore can roll back files and directories touched by the migration, including settings, SQLite state, extension metadata, copied extension folders, profile data, history, workspace state, Gemini data, and root app-state folders.

## Quick Start

1. Close Antigravity and Antigravity IDE.
2. Run a dry run:

   ```bash
   ./run-dry-run.command
   ```

3. Run the migration:

   ```bash
   ./run-migration.command
   ```

4. Open Antigravity IDE and verify settings, extensions, history, and workspace state.

## Recovery

Restore from a backup:

```bash
./run-restore.command "/path/to/migration_backups/<timestamp>"
```

Clean migration backups:

```bash
./run-cleanup.command
```

## Manual CLI

```bash
python3 -m src.main --dry-run --verbose
python3 -m src.main
python3 -m src.main --restore "/path/to/migration_backups/<timestamp>"
python3 -m src.main --cleanup
```

## Requirements

- macOS
- Python 3.8+
- no third-party Python packages

## Development

Run the unit tests:

```bash
python3 -m unittest tests/test_migration.py
```

## Project Notes

This is a standalone public utility. It is not part of MemFlow or the CPUcoin website codebase.

## Upstream

This macOS version was adapted from winteryu21's original Antigravity IDE migration utility. The original project focused on Windows migration support; this repository provides the macOS companion version with macOS paths, launchers, profile-state migration, and full migration-target rollback.

The intended community positioning is:

- original Windows migrator: upstream Windows-focused project
- this repository: macOS version maintained for the community under the CPUcoin GitHub organization

## License

MIT. See [LICENSE](./LICENSE).
