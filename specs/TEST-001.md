# TEST-001: Add `slugify()` to strutils

## Summary
Add a `slugify` function to the `strutils` package that converts arbitrary
text into a URL-safe slug.

## Requirements
- New function `slugify(text: str) -> str` in `strutils/__init__.py`.
- Behavior:
  - Lowercase the input.
  - Strip leading/trailing whitespace.
  - Replace any run of whitespace or underscores with a single hyphen `-`.
  - Remove any character that is not `a-z`, `0-9`, or `-`.
  - Collapse multiple consecutive hyphens into a single `-`.
  - Strip leading/trailing hyphens from the result.
  - `slugify("")` returns `""`.
- Examples:
  - `slugify("Hello, World!")` -> `"hello-world"`
  - `slugify("  Foo__Bar  ")` -> `"foo-bar"`
  - `slugify("a---b")` -> `"a-b"`
  - `slugify("!!!")` -> `""`

## Testing
- Add tests in `tests/test_strutils.py` covering every example above plus the
  empty-string and all-symbols edge cases.
- All tests must pass via `python3 -m unittest discover`.

## Out of scope
- Unicode transliteration (accented characters). ASCII only for now.
