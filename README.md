# Wolt Summer Eng Assignment

[![PyPI](https://img.shields.io/pypi/v/wolt-summer-eng-assignment.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/wolt-summer-eng-assignment.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/wolt-summer-eng-assignment)][python version]
[![License](https://img.shields.io/pypi/l/wolt-summer-eng-assignment)][license]

[![Read the documentation at https://wolt-summer-eng-assignment.readthedocs.io/](https://img.shields.io/readthedocs/wolt-summer-eng-assignment/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/hiAndrewQuinn/wolt-summer-eng-assignment/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/hiAndrewQuinn/wolt-summer-eng-assignment/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/wolt-summer-eng-assignment/
[status]: https://pypi.org/project/wolt-summer-eng-assignment/
[python version]: https://pypi.org/project/wolt-summer-eng-assignment
[read the docs]: https://wolt-summer-eng-assignment.readthedocs.io/
[tests]: https://github.com/hiAndrewQuinn/wolt-summer-eng-assignment/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/hiAndrewQuinn/wolt-summer-eng-assignment
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

Hi! I'm Andrew, and this is my attempt at the [Python backend preliminary coding assignment](https://github.com/woltapp/engineering-summer-intern-2023) for Wolt. I like animated screenshots, so here's an example of my solution in action:

![Demo with 4 multiplexed screens of code. Upper left shows the web server running; lower left shows the content of a request payload I'm sending with a simple Bash script. Lower right shows a 2 second loop of the response payload of the lower right, which I change in real time. Upper right shows the results of the pytest and miscellaneous information.](https://user-images.githubusercontent.com/53230903/216786616-c4c7be95-0f5d-4ea2-8ef8-aad03fc6a60b.svg)

(You can see an identical SVG in the `demo.svg` of this file as well, although generally speaking I don't like committing large files like that to repos.)

# Quickstart

First install [Poetry](https://python-poetry.org/docs/) however you wish. Then run

```python
poetry install
poetry run wolt-summer-eng-assignment --help
```

Then go ahead and send your payloads to whatever port it assigns you, most likely `localhost:8000`.

## Features

This is just a preliminary assignment, but here are some directions I could go.

- *Figure out a way to test the server code in `__main__.py`.* I factored out the business logic to `logic.py` and
  have that tested fairly well (writing those unit tests actually showed me a lot of flaws in my original thinking),
  but I don't have anything in place testing the FastAPI code itself yet. I'm not doing anything fancy with it but
  it would be nice.
- *Fix everything `nox` complains about.* I do `poetry run pytest` in the animated SVG but that's actually just the
  tip of the iceberg. You can run `nox` on this repo to see _a lot_ more places where things can be fixed,
  dependency patches could be applied, etc.
- *Use types!* `mypy` exists in here and would probably make this look much more professional if I were to use it.

## Requirements

All documented in [Wolt's "Specifications" section](https://github.com/woltapp/engineering-summer-intern-2023#specification).

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/hiAndrewQuinn/wolt-summer-eng-assignment/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/hiAndrewQuinn/wolt-summer-eng-assignment/blob/main/LICENSE
[contributor guide]: https://github.com/hiAndrewQuinn/wolt-summer-eng-assignment/blob/main/CONTRIBUTING.md
[command-line reference]: https://wolt-summer-eng-assignment.readthedocs.io/en/latest/usage.html
