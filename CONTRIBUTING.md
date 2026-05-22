# Contributing

Contributions are welcome for macOS migration reliability, documentation, tests, and safety improvements.

## Scope

This repository is the macOS version of the Antigravity IDE migration utility. Keep changes focused on:

- macOS path resolution
- migration safety
- backup and restore behavior
- profile, workspace, history, extension, Gemini, and SQLite data handling
- clear user-facing documentation

Do not add network services, telemetry, package downloads, or remote execution.

## Reporting Issues

Please include:

- macOS version
- Antigravity and Antigravity IDE versions, if known
- whether both apps were closed before migration
- whether the issue happens in dry-run or real migration
- relevant `migration.log` lines

Do not paste private conversation content or secrets from migrated files.

## Pull Requests

Before opening a pull request:

```bash
python3 -m unittest tests/test_migration.py
```

Keep the project dependency-free. It should continue to use only the Python standard library.

## License

By contributing, you agree that your contributions are licensed under the MIT License.
