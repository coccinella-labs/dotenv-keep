# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-08-07

### Added

- `.env` parser handling comments, quotes, `export`, and inline comments.
- Reference scanner for `os.environ["NAME"]`, `os.getenv("NAME")`, and
  `process.env.NAME`.
- `missing`/`unused` reporting in the `dotenv-keep` CLI.
- Library API: `load`, `parse_env`, `find_references`, and `compare`.
