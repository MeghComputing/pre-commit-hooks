## Development setup

### Python virtual environment

Lets assume you start with python, pip, and python-venv installed.

`python3 -m venv env` will create a new directory named `env` and install a new virtual environment in it.

Activate the environment with`. env/bin/activate`.

Deactivate the environment when you're done with `deactivate`.

### Upgrade pip

With your virtual environment activated, first upgrade pip to the latest version with

`pip install --upgrade pip`. Pip should be at least version 21.3.1.

### Install dependencies

Now install this repo as a package along with its development dependencies with `pip install -e '.[dev]'`. The `-e` option installs the package as "editable"--any changes you make in the source code will immediately be reflected in the environment without having to reinstall the package.

The package can be uninstalled with `pip uninstall megh-pch` if needed.

## Unit tests

Simply run `pytest` and it should pickup on the tests to run.

## Linting

Use `pre-commit run --all-files` to run linting on all files.

If you want to run your local changes, use `pre-commit try-repo . --all-files`.

If you want to run on only the files that have changed since `<hash>`, try:

`pre-commit run --files $(git diff --diff-filter=ACMRT --name-only --no-ext-diff -z <hash> | xargs --null)`

 `<hash>` can be, for example, `961ac74`, `develop`, `2022.1`, or `HEAD~1`.

## Packaging development

Adding new scripts, changing the directory structure, and adding requirements will require updating the packaging configuration. In order to run as a "language: python" pre-commit script, this project has to be installable with pip via `pip install .`.

A `pyproject.toml` was chosen over a `setup.py` file because it's going to be the new standard way. Also, this project is small and simple enough that `pyproject.toml`is sufficient, regardless of how mature the support is. Flit's website is https://flit.pypa.io/en/latest/pyproject_toml.html.

Current popular build tools that can use a `pyproject.toml` are Setuptools (also the de facto standard for `setup.py`), Poetry, and Flit. Flit was chosen because it suppports the `-e` option for editable pip installs mentioned earlier.

Scripts are mapped under the `[project.scripts]` table. These deploy a shell script in the env that will invoke the given function.

Requirements are given in the `project.dependencies` list. These are installed along with the project with `pip install .`. Optional dependencies are installed with `pip install '.[OPTION]'`.

A wheel can be built with `flit build` after an initial `pip install flit`.
