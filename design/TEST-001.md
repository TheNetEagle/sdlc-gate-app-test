# TEST-001 Implementation Plan: Add `slugify()` to strutils

## Overview
Add a pure, dependency-free `slugify(text: str) -> str` function to the
`strutils` package that converts arbitrary text into a URL-safe ASCII slug.
This is an additive change with no impact on existing behavior.

## Existing architecture & conventions
- `strutils/__init__.py` is a single flat module. Functions are module-level,
  typed (`def reverse(s: str) -> str:`), with a one-line `"""docstring"""`.
- No third-party dependencies; standard library only. `slugify` should stay
  dependency-free and may use the stdlib `re` module.
- Tests live in `tests/test_strutils.py` using `unittest`, one `TestCase` class
  per function (`TestReverse`). Run via `python3 -m unittest discover`.
- No `docs/adr` directory exists, so there are no ADRs to conform to.

## Affected components
- `strutils/__init__.py` — add the `slugify` function (and `import re` at the
  top of the module). No changes to `reverse`.
- `tests/test_strutils.py` — add a new `TestSlugify(unittest.TestCase)` class
  mirroring the existing `TestReverse` style.
- No changes to `README.md` are required; the test command is unchanged.

## Data model changes
None. This is a pure function operating on strings; there is no persistent
state, schema, or storage involved.

## API / interface changes
Add one public function to the `strutils` package:

```python
def slugify(text: str) -> str:
    """Convert text into a URL-safe ASCII slug."""
```

Processing order (derived directly from the spec, sequenced to be
self-consistent):
1. Lowercase the input.
2. Strip leading/trailing whitespace.
3. Replace any run of whitespace or underscores with a single hyphen `-`.
4. Remove any character not in `[a-z0-9-]`.
5. Collapse multiple consecutive hyphens into a single `-`.
6. Strip leading/trailing hyphens.
7. `slugify("")` returns `""` (falls out naturally from the above).

Reference implementation sketch (for the code agent; not binding):

```python
import re

def slugify(text: str) -> str:
    """Convert text into a URL-safe ASCII slug."""
    text = text.strip().lower()
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"[^a-z0-9-]", "", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")
```

Note: steps 3 and 4 interact — replacing whitespace/underscores with hyphens
*before* stripping disallowed characters ensures word boundaries survive as
hyphens rather than being deleted. The final collapse + strip handles hyphens
introduced by removed characters (e.g. `"Hello, World!"` → `"hello,-world!"`
→ `"hello--world"` → `"hello-world"`).

## Test strategy
Add `TestSlugify` in `tests/test_strutils.py` covering every spec example plus
edge cases:

| Input            | Expected   | Case covered              |
|------------------|------------|---------------------------|
| `"Hello, World!"`| `"hello-world"` | punctuation + space  |
| `"  Foo__Bar  "` | `"foo-bar"`| leading/trailing ws, underscores |
| `"a---b"`        | `"a-b"`    | hyphen collapse           |
| `"!!!"`          | `""`       | all-symbols → empty       |
| `""`             | `""`       | empty string              |

Consider one extra assertion for a leading/trailing-hyphen strip case
(e.g. `"-hi-"` → `"hi"`) to lock in step 6.

All tests must pass via `python3 -m unittest discover` with zero new
dependencies.

## Rollout considerations
- Purely additive: `reverse` and its test are untouched, so there is no
  backward-compatibility risk.
- No migrations, feature flags, or config changes.
- No versioning/packaging metadata exists in the repo to bump.
- Merge gate: the full `unittest discover` suite must be green.

## Out of scope
- Unicode transliteration / accented-character folding (e.g. `café` → `cafe`).
  ASCII-only per the spec.
- Configurable separators, max-length truncation, or stop-word removal.
- Uniqueness/deduplication of slugs against any external store.
- Changes to `reverse`, `README.md`, or the packaging/CI setup.
