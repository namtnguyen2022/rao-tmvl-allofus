#!/usr/bin/env python3
"""Check the Git index for generated data, executed notebooks, and obvious secrets.

This is a publication guard, not an All of Us disclosure-review substitute.
Uses only the standard library and never executes analysis cells.
"""
from __future__ import annotations

import ast
import csv
import io
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
DEFINITIONS = 'definitions/procedure_concepts.csv'
FIELDS = ['concept_id', 'concept_name', 'vocabulary_id', 'concept_code', 'test', 'include', 'review_note']
BLOCKED_DIRS = {'data', 'internal', 'results', '.ipynb_checkpoints'}
BLOCKED_EXTENSIONS = {'.csv', '.tsv', '.parquet', '.feather', '.pkl', '.pickle', '.rds', '.rdata',
                      '.html', '.pdf', '.docx', '.png', '.jpg', '.jpeg', '.svg', '.zip'}
SECRET_PATTERNS = [
    r'gh[pousr]_[A-Za-z0-9]{20,}',
    r'github_pat_[A-Za-z0-9_]{20,}',
    r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    r'"type"\s*:\s*"service_account"',
]


def check_file(name: str, content: bytes) -> list[str]:
    path = PurePosixPath(name)
    errors = []
    if (set(path.parts) & BLOCKED_DIRS or 'INTERNAL' in name.upper()
            or (path.suffix.lower() in BLOCKED_EXTENSIONS and name != DEFINITIONS)):
        errors.append(f'{name}: generated data or output format is not allowed')
    if path.name.startswith('.env') and path.name != '.env.example':
        errors.append(f'{name}: local environment file is not allowed')
    if path.suffix.lower() in {'.key', '.pem'} or path.name in {'.Renviron', '.Rhistory'}:
        errors.append(f'{name}: local credentials or session file is not allowed')
    if len(content) > 2_000_000:
        errors.append(f'{name}: unexpectedly large file; inspect before publishing')
    try:
        text = content.decode('utf-8')
    except UnicodeDecodeError:
        return errors + [f'{name}: unexpected binary file']
    if any(re.search(pattern, text) for pattern in SECRET_PATTERNS):
        errors.append(f'{name}: possible secret; value intentionally not printed')
    if re.search(r'/' + r'Users/[^/\s]+/|' + r'gs:' + r'//[^\s\"\']+', text):
        errors.append(f'{name}: local user path or bucket URI found')
    if name == DEFINITIONS:
        reader = csv.DictReader(io.StringIO(text))
        if reader.fieldnames != FIELDS:
            errors.append(f'{name}: only count-free definition columns are allowed')
        else:
            for row in reader:
                if row['test'] not in {'echo', 'rhythm', 'carotid', 'brain'}:
                    errors.append(f'{name}: unrecognized test family')
                if row['include'].lower() not in {'true', 'false'}:
                    errors.append(f'{name}: invalid inclusion flag')
                if row['concept_code'] in {'93313', '93316'} and row['include'].lower() != 'false':
                    errors.append(f'{name}: probe-placement-only code must remain excluded')
    if path.suffix == '.ipynb':
        try:
            notebook = json.loads(text)
            language = notebook.get('metadata', {}).get('kernelspec', {}).get('language', '')
            if set(notebook.get('metadata', {})) - {'kernelspec', 'language_info'}:
                errors.append(f'{name}: unexpected notebook metadata')
            for i, cell in enumerate(notebook['cells']):
                if cell.get('outputs') or cell.get('execution_count') is not None:
                    errors.append(f'{name}: cell {i} has saved execution data')
                if cell.get('attachments') or cell.get('metadata'):
                    errors.append(f'{name}: cell {i} contains attachments or metadata')
                if cell['cell_type'] == 'code' and language == 'python':
                    ast.parse(''.join(cell['source']))
        except (ValueError, KeyError, SyntaxError) as exc:
            errors.append(f'{name}: invalid notebook or Python source ({type(exc).__name__})')
    return errors


def main() -> int:
    names = subprocess.check_output(['git', 'ls-files', '--cached', '-z'], cwd=ROOT).decode().split('\0')
    names = [name for name in names if name]
    if not names:
        print('No staged/tracked files found; stage the intended publication files first.')
        return 1
    errors = []
    for name in names:
        # Read the index, so an unexecuted working copy cannot hide staged outputs.
        content = subprocess.check_output(['git', 'show', f':{name}'], cwd=ROOT)
        errors.extend(check_file(name, content))
    if errors:
        print('\n'.join(errors))
        return 1
    print(f'PASS: {len(names)} indexed files checked; notebooks are unexecuted and definitions are count-free.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
