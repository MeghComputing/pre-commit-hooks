# pre-commit-hooks

This repo is for Megh's custom pre-commit hooks.

## copyrighter

[copyrighter](/megh_pch/copyrighter/) is a script that checks the copyright head in a given file. It detects detects if the header is missing. It can also detect if the year does not match the current year, and can automatically update it.

## Development and testing

See [tests/README.md](/tests/) for documentation on setting up a development environment and running tests for this repo.

## Hooks

Hooks are exported in the `.pre-commit-hooks.yaml` file for use in other repos. To use, add them to the `.pre-commit-config.yaml` file in the root of your repo. For an example, see this repo's [`.pre-commit-config.yaml`](/.pre-commit-config.yaml). pre-commit's documentation is at https://pre-commit.com/.

## GitHub Actions

See this repo's [`.github/workflows/linting.yaml`](/.github/workflows/linting.yaml) file for example of adding pre-commit to GitHub Actions.
