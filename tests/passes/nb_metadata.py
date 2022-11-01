import sys
import nbformat
import subprocess
from pathlib import Path
from tools import parse_args


CLEAN_METADATA = {'kernelspec': {'display_name': 'Python 3',
  'language': 'python',
  'name': 'python3'},
  'language_info': {'codemirror_mode': {'name': 'ipython', 'version': 3},
  'file_extension': '.py',
  'mimetype': 'text/x-python',
  'name': 'python',
  'nbconvert_exporter': 'python',
  'pygments_lexer': 'ipython3',
  'version': '3.9'}}


def check_metadata(filepath, fix=False):
    notebook = nbformat.read(filepath, 4)
    if notebook.metadata == CLEAN_METADATA:
        return True
    elif fix:
        notebook.metadata = CLEAN_METADATA
        nbformat.write(notebook, filepath)
        return True
    else:
        raise ValueError(
            f'Bad metadata in {filepath}.\nRun `python '
             'tests/passes/nb_metadata.py --fix` to reset, '
             'or see tests/README.md for more info.'
        )

if __name__ == '__main__':
    # usage: python nb_metadata.py --fix notebook1.ipynb path/to/notebook2.ipynb
    switches, filepaths = parse_args(sys.argv)

    fix = '--fix' in switches
    git_add = '--git-add' in switches

    for path in filepaths:
        check_metadata(path, fix)
        if git_add:
            subprocess.run(['git', 'add', path])
