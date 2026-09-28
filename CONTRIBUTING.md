# Contributing

Keep this repository limited to analysis source code, count-free concept definitions,
and documentation. Run the study only within an authorized All of Us Workbench.

Before committing, remove notebook outputs, execution counts, cell metadata, and
attachments. Never commit participant-level data, source-code frequency audits,
generated results, credentials, or executed HTML exports. `.gitignore` is a guard
against accidents, not a substitute for review.

Enable the local publication hook after cloning:

```sh
git config core.hooksPath .githooks
```

Stage the intended code changes, then check the staged content:

```sh
python scripts/check_repository.py
python scripts/test_publication_guard.py
```

The same checks run in GitHub Actions. Passing them verifies repository packaging
and Python syntax, not scientific validity, All of Us disclosure compliance, or
successful execution against the restricted dataset. Review every staged diff.

For methodological changes, record the rationale and specify whether the change
alters cohort membership, endpoint definitions, follow-up, model adjustment, or
disclosure handling. Preserve provenance for the exact definitions used in a run.
