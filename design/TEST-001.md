# TEST-001 Implementation Plan: Add `slugify()` to strutils

## Overview
Add a pure, dependency-free `slugify(text: str) -> str` function to the
`strutils` package that converts arbitrary text into a URL-safe ASCII slug,
per the requirements in `specs/TEST-001.md`.

## Current architecture & conventions
The codebase is intentionally minimal:

- `strutils/__init__.py` — single module holding public functions. Currently
  exposes `reverse(s: str) -> str`. Functions are top-level, fully type-hinted,
  and carry a one-line docstring.
- `tests/test_strutils.py` — `unittest`-based tests. Imports functions by name
  from `strutils`, groups them in a `TestCase` subclass, uses
  `self.assertEqual`. Run via `python3 -m unittest discover`.
- No external dependencies; standard library only. `re` is available and is the
  natural fit for this task.
- No `docs/adr` directory exists, so there are no ADRs to conform to. The
  design follows the established repo conventions above.

## Affected components
- **`strutils/__init__.py`** — add the new `slugify` function alongside
  `reverse`. Add `import re` at the top of the module.
- **`tests/test_strutils.py`** — add a `TestSlugify` `TestCase` and import
  `slugify`.

No other files are affected.

## Data model changes
None. This is a pure, stateless string transformation with no persistence,
state, or shared data structures.

## API / interface changes
New public function:

```python
def slugify(text: str) -> str:
    """Convert text into a URL-safe ASCII slug."""
```

Contract (order-sensitive, mirroring the spec):
1. Lowercase the input.
2. Strip leading/trailing whitespace.
3. Replace any run of whitespace or underscores with a single hyphen `-`.
4. Remove any character that is not `a-z`, `0-9`, or `-`.
5. Collapse multiple consecutive hyphens into a single `-`.
6. Strip leading/trailing hyphens from the result.
7. `slugify("")` returns `""`.

Suggested implementation approach (regex-based, stdlib only):

```python
def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[\s_]+", "-", text)      # whitespace/underscore runs -> "-"
    text = re.sub(r"[^a-z0-9-]", "", text)   # drop disallowed characters
    text = re.sub(r"-+", "-", text)          # collapse hyphen runs
    return text.strip("-")                    # trim leading/trailing hyphens
```

Note on ordering: removing disallowed characters (step 4) happens *after*
whitespace→hyphen (step 3) so separators are preserved, and *before* the
hyphen collapse (step 5) so any hyphens exposed by removal are collapsed. This
correctly handles `"a---b"` -> `"a-b"` and `"!!!"` -> `""`.

This is a non-breaking, purely additive change — `reverse` and its callers are
untouched.

## Test strategy
Add `TestSlugify` to `tests/test_strutils.py` covering every spec example plus
edge cases:

| Input | Expected |
|-------|----------|
| `"Hello, World!"` | `"hello-world"` |
| `"  Foo__Bar  "` | `"foo-bar"` |
| `"a---b"` | `"a-b"` |
| `"!!!"` | `""` |
| `""` | `""` |

Additional edge cases worth asserting for robustness:
- Mixed whitespace runs (tabs/newlines/spaces) collapse to a single hyphen.
- Already-slugified input is idempotent: `slugify("hello-world") == "hello-world"`.
- Leading/trailing symbols that reduce to hyphens are stripped, e.g.
  `slugify("-Hello-") == "hello"`.

Verify all tests pass with `python3 -m unittest discover` before handoff to the
code/review loop.

## Rollout considerations
- No migration, feature flag, or config change required — additive stdlib-only
  function.
- No runtime dependencies introduced; no version bump semantics beyond a normal
  minor addition.
- Backward compatible: no existing signatures change.
- Risk is low and isolated to the new function; regression surface is limited
  to the `strutils` public API surface, which the test suite covers.

## Out of scope
- Unicode transliteration / accent folding (e.g. `é` -> `e`). ASCII-only per the
  spec; non-ASCII letters are simply dropped by step 4.
- Configurable separators, max-length truncation, or stop-word removal.
- Uniqueness/collision handling (e.g. appending numeric suffixes) — `slugify` is
  a pure transform with no knowledge of other slugs.
- Any changes to `reverse` or the packaging/build setup.
