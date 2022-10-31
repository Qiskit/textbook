import sys
import nbformat
import subprocess
from scour import scour
from tools import parse_args


class ScourOptions:
    def __init__(self, **entries):
        self.__dict__.update(entries)


SCOUR_OPTIONS = ScourOptions(
    **{
        'simple_colors': False,
        'style_to_xml': True,
        'group_collapse': True,
        'group_create': True,
        'keep_editor_data': False,
        'keep_defs': False,
        'renderer_workaround': True,
        'strip_xml_prolog': False,
        'remove_titles': True,
        'remove_descriptions': True,
        'remove_metadata': True,
        'remove_descriptive_elements': True,
        'strip_comments': True,
        'enable_viewboxing': True,
        'indent_type': 'none',
        'newlines': False,
        'strip_xml_space_attribute': False,
        'strip_ids': True,
    }
)


def scour_svgs(filepath, fix=False):
    """Search through notebook and find/replace un-minimized SVGs"""
    notebook = nbformat.read(filepath, 4)
    needs_write = False
    for cell in notebook.cells:
        if cell.cell_type == 'code':
            for output in cell.outputs:
                if 'data' in output:
                    if 'image/svg+xml' in output['data']:
                        svg = output['data']['image/svg+xml']
                        if '\n' in svg:
                            if fix:
                                needs_write = True
                                min_svg = scour.scourString(svg, SCOUR_OPTIONS)
                                min_svg = min_svg.replace('\n', '')
                                output['data']['image/svg+xml'] = min_svg
                            else:
                                raise ValueError(f'Error in {filepath}: SVG not minified.\n'
                                                  'Run `python tests/passes/nb_svg.py --fix'
                                                  '` to fix, or see tests/README.md for more'
                                                  ' info.')
    if fix and needs_write:
        nbformat.write(notebook, filepath, 4)


if __name__ == '__main__':
    # usage: python nb_svg.py --fix notebook1.ipynb path/to/notebook2.ipynb
    switches, filepaths = parse_args(sys.argv)

    fix = '--fix' in switches
    git_add = '--git-add' in switches

    for path in filepaths:
        scour_svgs(path, fix)
        if git_add:
            subprocess.run(['git', 'add', path])
