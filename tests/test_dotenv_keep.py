import pytest

from dotenv_keep import compare, find_references, load, parse_env, parse_line


def test_parse_line_basic():
    assert parse_line("FOO=bar") == ("FOO", "bar")


def test_parse_line_skips_comments_and_blanks():
    assert parse_line("") is None
    assert parse_line("   ") is None
    assert parse_line("# comment") is None
    assert parse_line("not a pair") is None


def test_parse_line_handles_export_and_quotes():
    assert parse_line("export FOO=bar") == ("FOO", "bar")
    assert parse_line("FOO='bar'") == ("FOO", "bar")
    assert parse_line('FOO="bar"') == ("FOO", "bar")


def test_parse_line_strips_inline_comments():
    assert parse_line("FOO=bar # keep this") == ("FOO", "bar")


def test_parse_env():
    env = parse_env(
        "API_URL=https://example.com\n# comment\nEMPTY=\nexport TOKEN=abc\n"
    )
    assert env == {"API_URL": "https://example.com", "EMPTY": "", "TOKEN": "abc"}


def test_find_references():
    text = (
        "os.environ['API_KEY'] and os.getenv(\"DATABASE_URL\") "
        "and process.env.NODE_ENV and something_else"
    )
    assert find_references(text) == {"API_KEY", "DATABASE_URL", "NODE_ENV"}


def test_compare_reports_missing_and_unused():
    example = {"PRESENT": "1", "UNUSED": "1"}
    refs = {"PRESENT", "MISSING"}
    missing, unused = compare(example, refs)
    assert missing == {"MISSING"}
    assert unused == {"UNUSED"}


def test_load(tmp_path):
    env_file = tmp_path / ".env.example"
    env_file.write_text("FOO=bar\n", encoding="utf-8")
    assert load(env_file) == {"FOO": "bar"}
