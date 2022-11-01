import re
import sys
import time
import nbformat
import nbconvert
from datetime import datetime
from tools import parse_args, style, indent


class ExecutePreprocessor(nbconvert.preprocessors.ExecutePreprocessor):
    """Need custom preprocessor to skip `uses-hardware` cells"""
    def preprocess_cell(self, cell, resources, cell_index):
        if hasattr(cell.metadata, 'tags'):
            if 'uses-hardware' in cell.metadata.tags:
                # Skip execution
                return cell, resources
        return super().preprocess_cell(cell, resources, cell_index)


def timestr():
    """Get current time (for reporting in terminal)"""
    timestr = f"[{datetime.now().time().strftime('%H:%M')}]"
    return style('faint', timestr)


def contains_code_cells(notebook):
    for cell in notebook.cells:
        if cell.cell_type == 'code':
            return True
    return False


def format_message_terminal(msg):
    """Formats error messages nicely for the terminal"""
    outstr = style(msg['severity'], msg['name'])
    outstr += f": {msg['description']}"
    if 'code' in msg:
        outstr += "\nError occurred as result of the following code:\n"
        outstr += indent(msg['code'])
    return outstr


def get_warnings(cell):
    """Returns any warning messages from a cell's output"""
    warning_messages = []
    for output in cell.outputs:
        if hasattr(output, 'name') and output.name == 'stderr':
            try:  # Try to identify warning type
                warning_name = re.search(r'(?<=\s)([A-Z][a-z0-9]+)+(?=:)',
                                         output.text)[0]
                description = re.split(warning_name,
                                        output.text,
                                        maxsplit=1)[1].strip(' :')
            except TypeError:
                warning_name = 'Warning'
                description = output.text

            warning_messages.append({'name': warning_name,
                                     'severity': 'warning',
                                     'description': description,
                                     'full_output': output.text})
    return warning_messages



def run_notebook(filepath, write=False, fail_on_warning=False):
    """Attempts to run a notebook and return any error / warning messages.
    Args:
        filepath (Path): Path to the notebook
        write (bool): Whether to write the updated outputs to the file.
    Returns:
        bool: True if notebook executed without error, False otherwise.
              (Note: will not write if there are any errors during execution.)
        list: List of dicts containing error / warning message information.
    """
    execution_success = True
    messages = []  # To collect error / warning messages

    with open(filepath) as f:
        notebook = nbformat.read(f, as_version=4)

    if not contains_code_cells(notebook):
        # Avoid creating new kernel for no reason
        return True, messages

    # Clear outputs
    processor =  nbconvert.preprocessors.ClearOutputPreprocessor()
    processor.preprocess(notebook,
                         {'metadata': {'path': filepath.parents[0]}})

    # Execute notebook
    processor = ExecutePreprocessor(timeout=None)
    try:
        processor.preprocess(notebook,
                             {'metadata': {'path': filepath.parents[0]}})
    except Exception as err:
        err_msg = {'name': err.ename,
                   'severity': 'error',
                   'description': err.evalue,
                   'code': err.traceback.split('------------------')[1],
                   'full_output': err.traceback
                   }
        messages.append(err_msg)
        execution_success = False

    # Search output for warning messages (can't work out how to get the kernel
    # to report these)
    for cell in notebook.cells:
        if cell.cell_type != 'code':
            continue

        ignore_warning_tag = (hasattr(cell.metadata, 'tags')
                     and 'ignore-warning' in cell.metadata.tags)

        warning_messages = get_warnings(cell)
        if not ignore_warning_tag:
            messages += warning_messages
            if fail_on_warning and (messages!=[]):
                execution_success = False

        # Clean up unused tags if warning disappears
        if ignore_warning_tag and (warning_messages == []):
            cell.metadata.tags.remove('ignore-warning')

    # Remove useless execution metadata
    for cell in notebook.cells:
        if 'execution' in cell.metadata:
            del cell.metadata['execution']

    if execution_success and write:
        with open(filepath, 'w', encoding='utf-8') as f:
            nbformat.write(notebook, f)

    return execution_success, messages


if __name__ == '__main__':
    # usage: python nb_autorun.py --write --fail-on-warning notebook1.ipynb path/to/notebook2.ipynb
    switches, filepaths = parse_args(sys.argv)

    write, fail_on_warning = False, False
    for switch in switches:
        if switch == '--write':
            write = True
        if switch == '--fail-on-warning':
            fail_on_warning = True

    log = {'t0': time.time(),
            'total_time': 0,
            'total_files': 0,
            'broken_files': 0
          }

    # Start executing notebooks
    print('\n\033[?25l', end="")  # hide cursor
    for path in filepaths:
        log['total_files'] += 1
        print('-', timestr(), path, end=' ', flush=True)

        success, messages = run_notebook(path, write, fail_on_warning)
        if success:
            print("\r" + style('success', '✔'))
        else:
            log['broken_files'] += 1
            print("\r" + style('error', '✖'))

        if messages:
            message_strings = [format_message_terminal(m) for m in messages]
            print(indent('\n'.join(message_strings)))

    print('\033[?25h', end='')  # un-hide cursor

    # Display output and exit
    log['total_time'] = time.time()-log['t0']
    print(f"Finished in {log['total_time']:.2f} seconds\n")
    if log['broken_files'] > 0:
        print(f"Found problems in {log['broken_files']}/{log['total_files']} "
               "notebooks, see output above for more info.\n")
        if fail_on_warning:
            print("If this test failed due to a new warning that is out of "
                  "scope of\nthis PR, please make a new issue describing the "
                  "warning, and add\nan `ignore-warning` tag to any problem "
                  "cells so your PR can pass\nthis test.\n")
        sys.exit(1)
    sys.exit(0)
