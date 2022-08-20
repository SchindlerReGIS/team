# TEAM: teach a robot arm to move

[![Build Status](https://dev.azure.com/devsdb/CRD-NT_ARCO/_apis/build/status/SchindlerReGIS.team?repoName=SchindlerReGIS%2Fteam&branchName=main)](https://dev.azure.com/devsdb/CRD-NT_ARCO/_build/latest?definitionId=1211&repoName=SchindlerReGIS%2Fteam&branchName=main)

TEAM is a parameter-free algorithm to learn motions from user demonstrations.
This proposed method has been submitted to [ICRA2023](https://www.icra2023.org/) and the paper can be found on arXiv.

If you use this work please cite:

> citation to come

## Build and Test

1. Install [flit](https://github.com/pypa/flit) with `pip install flit`.
We use flit to package and install this repository.
2. Clone/fork the repo from Github.
3. Run `pip install -e .` in the root folder to install rws2 in editable mode (`pip install .` is enough if you do not plan to contribute).

The library should then be installed and you should be able to call it in python with `import team`.

## How to use the package

See `notebook/pipeline.ipynb`.

## License

This work is under the GNU AFFERO GENERAL PUBLIC LICENSE.
If you would like to use this work under another LICENSE than this one, please contact us directly.

## Contribute

PR request on GitHub are welcome.
We use [black](https://github.com/psf/black) for code formatting and [flake8](https://github.com/pycqa/flake8) for linting.
Code that do not follow black formatting and follow flake8 linting will be rejected by the pipeline.

A standard git commit message consists of three parts, in order: a summary line, an optional bod.
The parts are separated by a single empty line.
The summary line is included in the short logs (git log --oneline, gitweb, Azure DevOps, email subject) and therefore should provide a short yet accurate description of the change.
The summary line is a short description of the most important changes. The summary line must not exceed 50 characters, and must not be wrapped. The summary should be in the imperative tense.
The body lines must not exceed 72 characters and can describe in more details what the commit does.
