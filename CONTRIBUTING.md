# Contributing

## Setup

```sh
git clone https://github.com/matiascostamagna/md-to-pdf.git
cd md-to-pdf
pip install -e ".[dev]"
md-to-pdf --install-browser
```

## Workflow

1. Create a branch: `git checkout -b feat/your-feature` or `fix/your-fix`
2. Make changes
3. Run tests: `pytest`
4. Commit using [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` new feature
   - `fix:` bug fix
   - `chore:` maintenance (deps, config, tooling)
   - `test:` adding or updating tests
   - `docs:` documentation only
5. Open a PR against `main`

## Rules

- Tests must pass before opening a PR — CI will block merges otherwise
- Every new feature or bug fix should include a test
- Keep PRs focused — one concern per PR
- No `print()` statements in library code; use `logging`

## Running tests

```sh
pytest            # all tests
pytest -k "conv"  # filter by name
pytest -v         # verbose
```

The integration test (`test_md_to_pdf_integration_produces_pdf`) is skipped
automatically when Chromium is not installed.
