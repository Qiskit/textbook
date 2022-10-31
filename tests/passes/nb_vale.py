"""This script runs 'prose linting' checks on the notebooks.
This includes spell checking, and writing best practices.
Requires Vale: https://vale.sh/docs/vale-cli/installation/
"""
import sys
import os
import shutil
import nbformat
import subprocess
import json
from pathlib import Path
from tools import parse_args, style, indent


NB_PATHS = './tests/notebook_paths.txt'
TEMP_DIR = './tests/.temp/md'
STYLE_DIR = './tests/style'


def lint_notebook(filepath, CI=False):
    """Perform Vale prose linting checks on
    notebook at `filepath`. If `CI` then exit
    early with code 1 on lint error."""
    print(style('bold', filepath))
    outdir = (
        Path(TEMP_DIR)
        / Path(filepath).parent.stem
        / Path(filepath).stem
    )
    extract_markdown(filepath, outdir)
    lint_markdown(outdir, CI)


def extract_markdown(filepath, outdir):
    """Extracts the markdown from the notebook
    at `filepath` and saves each cell as a separate
    file in the temp folder for Vale to lint."""
    nb = nbformat.read(filepath, as_version=4)
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    Path(outdir).mkdir(parents=True)
    for idx, cell in enumerate(nb.cells):
        if cell.cell_type == 'markdown':
            # outpath e.g.: ./scripts/temp/intro/grover-intro/0002.md
            outpath = Path(outdir) / (str(idx).rjust(4, '0') + '.md')
            with open(outpath, 'w+') as f:
                f.write(cell.source)


def lint_markdown(md_dir, CI=False):
    """Lints the markdown files in `md_dir`
    using Vale linter. If `CI`, then will exit with
    code 1 on any Vale error."""

    # Run Vale on folder
    files = os.listdir(md_dir)
    path = Path(md_dir)
    vale_result = subprocess.run(
        ['vale', path, '--output', 'JSON'],
        capture_output=True)
    vale_output = json.loads(vale_result.stdout)

    # Parse output and print nicely
    fail = False
    notebook_msg = ''
    for file, suggestions in vale_output.items():
        notebook_msg += f"cell {int(Path(file).stem)}\n"
        cell_msg = ''
        for s in suggestions:
            severity = s['Severity']
            if severity == 'error':
                fail = True
            cell_msg += style(severity, severity.capitalize())
            cell_msg += f": {s['Message']}\n"
            if s['Match'] != '':
                cell_msg += style('faint', f'"…{s["Match"]}…" ')
            cell_msg += style('faint', 
                f"@l{s['Line']};c{s['Span'][0]} ({s['Check']})")
            cell_msg += '\n'
        notebook_msg += indent(cell_msg) + '\n'
    if not CI and (notebook_msg!=''):
        print(indent(notebook_msg))
    if fail and CI:
        print(indent(notebook_msg))
        print(style('error', 'Prose linting error encountered; test failed.'))
        sys.exit(1)


if __name__ == '__main__':
    # usage: python3 nb_vale.py --CI notebook1.ipynb path/to/notebook2.ipynb
    switches, filepaths = parse_args(sys.argv)

    CI = '--CI' in switches

    for path in filepaths:
        lint_notebook(path, CI)
