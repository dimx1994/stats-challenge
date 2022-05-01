#!/usr/bin/env bash
# This script is intended to prettify code and run linters
CODE="app"

black $CODE --line-length=120
isort $CODE
flake8 --statistics $CODE
pylint --rcfile=setup.cfg $CODE
mypy --config-file mypy.ini $CODE