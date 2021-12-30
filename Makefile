.EXPORT_ALL_VARIABLES:

# so we're sure what shell we're using. Bash should be quite common, right?
SHELL:=/bin/bash

setup_workstation:
	python3 -m workstation_setup

# The below commands require setting up a virtualenv, activating it, and running `poetry install` in it.

validate_continously:
	fd '\.py$$' workstation_setup/ tests/ | entr -c make --keep-going validate

# Pylint can find errors in the code that can cause multiple tests to fail
# (which would produce a lot of pytest output), so we run it first.
# If we ran "test" first and got many test errors because of issues detectable by Pylint,
# analyzing the cause might take longer than if we saw the Pylint output
# (which we wouldn't get, since "make" normally stops processing on the first error).
validate: pylint test isort_check

test:
	@echo ===Tests===
	PYTHONPATH=.:configs/host_agnostic/bin pytest -v tests

pylint:
	@echo ===Pylint===
	pylint workstation_setup/ tests/

isort_check:
	@echo ===Isort===
	isort -c .
