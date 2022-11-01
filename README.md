# Qiskit Textbook content

This is the repository for the Qiskit Textbook's content. This page is for
people that want to contribute to the Textbook, if you just want to read about
quantum computing, go to qiskit.org/learn.

You'll need some software installed to work on this repo. We can install some
packages for you automatically, but you'll need to install the following
packages manually. You can do this now, or install each package as you need.

- [Python 3.8](https://www.python.org/): To run Qiskit and Jupyter notebook.
- [Git](https://git-scm.com): To save and share your changes.

These packages are not necessary, but may improve your experience working with
this repo:

- [Direnv](https://direnv.net/): To automatically switch environments when in
  this directory.
- [GitHub CLI](https://cli.github.com/): To easily work with github.com.
- [Vale linter](https://vale.sh/): Used for one of the tests.

## Jupyter notebooks

The source for each page in the textbook is a [Jupyter
notebook](https://jupyter.org/), a file format that combines
[Python](https://www.python.org/) code,
[markdown](https://www.markdownguide.org/basic-syntax/), and rich content (e.g.
images).

To make changes to the Qiskit Textbook, you will need to edit these notebooks,
then share your changes with us via GitHub. This section will show you how to
edit the notebooks in our repo, and the next section will guide you in sharing
your changes with us.

### Setting up

Firstly, you'll need to clone this repository. You'll need
[Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed,
and we recommend using the [GitHub CLI](https://cli.github.com/). To clone,
run:

```
gh repo clone Qiskit/textbook
```

Next, you'll need to install the specific packages we use in the textbook, and
set up your environment (you'll need [Python](https://www.python.org/)
already). To set up automatically, run:

```
./install.sh
```

<details>
  <summary> What does this do? </summary>

  <p>If you're interested, this script will:</p>

  <ul>
    <li>
    Setup a Python venv with the correct version of Python, and add a shell
    script to automatically switch to this venv when you move to this directory.
    </li>
    <li>
    Set up your IPython & Jupyter config so that your notebook outputs match
    those already in the textbook.
    </li>
    <li>
    Set up Git commit hooks that lint the notebooks to adhere to our conventions
    (this helps with reviewing PRs and merge conflicts).
    </li>
  </ul>
</details>

### Editing notebooks

To edit a notebook, navigate to this repo and run

```
jupyter notebook
```

then use the Jupyter notebook software to make your changes. You can check out [this
video](https://youtu.be/HW29067qVWk?t=243) if you're unfamiliar with notebooks.

The Qiskit Textbook also includes some extra features that we can't display in
the notebook editor. We use a special syntax to tell the Textbook website where
and how to insert these features. (TODO: include more about this).

## Git

- Why git? (todo)
- Guide on making a PR
- Guide on reviewing a PR
- Tests
- Git & notebooks

## Testing

When you submit a pull request (PR), we'll run some tests against your changes.
You can read more about them in the [`tests folder`](./tests).

## Versioning

We want to keep improving and updating the textbook, but many users (e.g.
professors teaching a course) want stable content that will not change. For
this reason, we release the Textbook content in _versions_, which are numbered
snapshots of the content that cannot change.

The version number tells you what kind of changes have been made from the
previous version. This repo follows a kind of [semantic
versioning](https://semver.org/), adapted to make more sense for non-code
repos.

For a verision number `MAJOR.MINOR.PATCH`, we will increment the:

- `MAJOR` version when changes remove or replace content,
- `MINOR` version for changes that add content, or that do not significantly
  alter the structure of existing pages. Examples include
    - adding new pages,
    - rewording paragraphs for clarity, and
    - small changes to code to make it work with newer Qiskit versions.
- `PATCH` version increments are for 'bugfixes' only. Examples include fixing
    - typos,
    - statements that are incorrect, and
    - code that does not work correctly with the version of Qiskit advertised
      on the page.

For example, if you're teaching using `v1.0.3`, you know you can switch to any
`v1.0.x` version without sections disappearing or code breaking with your
existing setup.

TODO: how to see diff between versions.
