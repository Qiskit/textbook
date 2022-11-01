# Automatic content checks

This repo includes scripts to automatically check (and sometimes fix) common
problems in the notebooks that hold the textbook content.

## Running tests

There are roughly three types of test, and you may only need to run some of
them depending on the changes you've made.

1. Notebook formatting tests.
   These tests check all notebooks follow consistent file formatting. This
   makes working with notebooks on GitHub easier. These tests are very fast
   and run as pre-commit hooks (added automatically by the `install.sh`
   script). To run manually (from repo root):
   ```
   ./tests/run_formatting.sh
   ```
2. Notebook content linting.
   These tests check the _content_ of the notebooks (i.e. the code in the code
   cells, and the writing in the markdown cells) for consistency. We check the
   code cells using [Pylint](https://github.com/PyCQA/pylint), and the markdown
   cells using [Vale](https://vale.sh/). See the "Files in the `passes` folder"
   section for more info. These tests are slower (can take a minute or two to
   run per notebook), so you can run them manually using
   ```
   ./tests/run_lint.sh
   ```
3. Notebook code testing.
   This test actually runs the notebooks to see if the code works. This can be
   very slow, as some of the notebooks take a _long_ time to execute. If you
   don't have reason to believe your changes will break any code, then you can
   let the GitHub action run this on your PR. This pass can also be used to
   update all notebooks (e.g. in the case of a Qiskit update). To do this, run 
   ```
   python ./tests/passes/nb_autorun.py --write
   ```

## Files in this folder

- `notebook_paths.txt`: Notebooks to run tests on.
  At the time of writing, not all notebooks pass the tests, and some will
  need a lot of work to get them to pass. For this reason, we only run
  checks on certain notebooks. If a notebook's path is not in this file,
  it will be ignored by `nb_lint` and `nb_vale`.

## Files in the `passes` folder

This folder contains different passes run over the notebooks.

- `toc.py`: Checks the table of contents (`notebooks/toc.yaml`) is valid.
  Other softwares outside this repo rely on information in `toc.yaml`. This
  script checks the file is valid, that all referenced files exist, and other
  things likely to go wrong.

- `nb_lint.sh`: Runs pylint on notebook code cells.
  The code examples in the textbook should meet the same standards as
  code in the Qiskit codebase. This script runs a pass/fail pylint check
  on each notebook.

  Since the code examples are not a code base, some rules don't apply,
  and we've tried to remove those where possible. You can also add a `
  pylint: disable=...` comment to avoid specific warnings (will be hidden
  on the site), but you should use this sparingly.

- `blips.py`: Check for important but easily fixable problems.
  - Each exercise should have a unique name, and we sometimes forget to update
    names when copying and pasting quizzes. This check fails if any quizzes
    share names.
  - Sometimes maintainers use the internal provider (`ibm-q-internal`) when
    updating cell outputs. This should be reset to the `ibm-q` provider before
    pushing. This check fails if it finds `ibm-q-internal` anywhere in the
    notebooks.

- `nb_metadata.py`: Checks (and resets) notebook metadata.
  The notebook metadata is largely useless and just tells you the
  environment of the last person to open the notebook. This makes git diffs
  messy, so all notebooks in the repo should have the same bland metadata.
  This script checks all metadata is the same, and you can pass `--fix` to
  overwrite the metadata. Running `install.sh` adds this as a commit hook.

- `nb_svg.py`: Clean SVGs in notebooks.
  We prefer notebook output images to be SVG as they produce clearer
  diagrams with smaller file sizes. The downside is that they produce
  large git diffs (lots of line changes), so we require that each SVG is
  optimized to a single line. This script checks the inline SVGs have been
  optimized, and can optimize any multi-line SVGs when run with the `--fix`
  argument. Running `install.sh` adds this as a commit hook.

- `nb_vale.py`: Run Vale linter checks on notebooks.
  [Vale](https://vale.sh/) is a 'prose linter', i.e. a program that checks
  for common problems in writing, including spelling errors, wordiness, and
  other writing malpractices. Since Vale (or any other prose linter) can't read
  notebooks, we use this script to pull the markdown from the notebooks to a
  temp folder, then run Vale on those files.

- `missing_nb_check.sh`: Compares files in old textbook repo to this repo.
  This script checks for notebooks added to `qiskit-community/qiskit
  textbook` that are not in `Qiskit/platypus` and makes a GitHub issue
  for it.

- `nb_autorun.py`: Script to run all the notebooks. Will report any errors, and
  will replace outputs if you pass `--write` option. This script can also
  optionally fail on warnings if passed `--fail-on-warning`. On PRs, this
  script runs on _any_ changed notebooks (not just those in
  `notebook_paths.txt`).

  Notebooks can include sanity checks on cell outputs; tagging these cells with
  `sanity-check` stops them appearing on the website. These cells should
  contain some kind of simple `assert` statement that checks the output of
  recent cells matches what's written in the text. This helps us catch
  unexpected code changes (e.g. from package updates, bugfixes in other parts
  of the notebook, or unlikely random samples). When adding a sanity check
  cell, you should include the quote from the main text that you're checking
  against. For example:
  ```
  # "...the output of the last cell is 0."
  assert _ == 0
  ```
  In Jupyter notebooks, `_` stores the last cell output. You can also use
  `Out[x]` to refer to specific cell outputs (assume all notebooks are run from
  top to bottom).

- `tools.py`: Shared logic (e.g. argument parsing) used by scripts in this
  folder.
