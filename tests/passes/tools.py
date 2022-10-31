"""This file contains functions shared by scripts in this folder
"""
import sys
from pathlib import Path

NB_ROOT = 'notebooks'
NB_PATHS_LIST = './tests/notebook_paths.txt'

def parse_args(argv):
    """Parses sys.argv to find notebook paths and switches, otherwise gets
    list of paths from `NB_PATHS_LIST`

    Returns a tuple with:
        - A set of switches (arguments starting with '--')
        - A list of filepaths
    """
    argv = argv[1:] if len(argv) > 1 else []

    switches = set()
    for a in argv:
        if a.startswith('--'):
            switches.add(a)
    
    filepaths = []
    for a in argv:
        if a not in switches:
            filepaths.append(a)

    if filepaths == []:
        # No files passed; read from text file
        with open(NB_PATHS_LIST, encoding='utf-8') as f:
            for path in f.readlines():
                path = path.strip()
                if path == '' or path.startswith('#'):
                    continue
                filepaths.append(path)

    # Make all paths of form ./notebook_root/folder/notebook.ipynb
    for idx, path in enumerate(filepaths):
        path = Path(path)
        if path.suffix == '':
            path = path.with_suffix('.ipynb')

        if not path.exists():
            path = Path(NB_ROOT) / path

        filepaths[idx] = path

    return switches, filepaths


TSTYLE = {  # Terminal styling codes
    'bold': '\033[1m',
    'faint': '\033[30m',
    'suggestion': '\033[94m',
    'warning': '\033[93m',
    'error': '\033[91m',
    'success': '\033[32m',
    'end': '\033[0m'
}


def style(style, text):
    """Style string using terminal escape codes"""
    return  f"{TSTYLE[style]}{text}{TSTYLE['end']}"


def indent(s):
    """Indent text block with vertical line margins"""
    s = s.replace('\n', '\n' + style('faint', '│ '))
    s = s[::-1].replace('│', '╵', 1)[::-1]
    return style('faint', '╷ ') + s
