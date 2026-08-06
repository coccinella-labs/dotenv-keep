# dotenv-keep

Keep environment variable names in sync across repos.

dotenv-keep compares your `.env.example` against the variables referenced
in your code and reports names that are missing, unused, or drifted. It
catches the silent misconfiguration that only shows up in production.

## Installation

```sh
pip install git+https://github.com/libnudget/dotenv-keep@v0.1.0
```

## Usage

```sh
dotenv-keep --example .env.example --path src
```

For each referenced variable that is missing from the example file, the
command prints a `missing:` line and exits with a non-zero status. It
also reports `unused:` names that appear in the example but are never
referenced in code.

## What it detects

- **Missing**: referenced in code as `os.environ["NAME"]`,
  `os.getenv("NAME")`, or `process.env.NAME`, but absent from the example
  file.
- **Unused**: present in the example file but never referenced in code.

## Library API

```python
from dotenv_keep import load, find_references, compare

example = load(".env.example")
refs = find_references(source_code_text)
missing, unused = compare(example, refs)
```

## Development

```sh
pip install -e ".[dev]"
pytest
```

## License

MIT
