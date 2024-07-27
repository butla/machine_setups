.EXPORT_ALL_VARIABLES:

# so we're sure what shell we're using. Bash should be quite common, right?
SHELL:=/bin/bash

SRC_DIRECTORIES:=machine_setup python_scripts_for_machine tests

LOG_PATH=/var/log

setup_machine:
	@echo "Ensuring a path for logs: $(LOG_PATH)"
	@sudo mkdir -p $(LOG_PATH)
	sudo bash -c "python3 -m machine_setup | tee --append $(LOG_PATH)/butla_upgrade.log"

setup_development:
	poetry install

# The below commands require setting up a virtualenv, activating it, and running `poetry install` in it.

# Static analysis can find errors in the code that can cause multiple tests to fail
# (which would produce a lot of pytest output), so we run it first.
# If we ran "test" first and got many test errors because of issues detectable by Pylint,
# analyzing the cause might take longer than if we saw the Pylint output
# (which we wouldn't get, since "make" normally stops processing on the first error).
check: static_analysis test

check_continously:
	# --keep-going instructs "make" to not stop on the first command that fails, so we get a result for all the checks
	fd '\.py$$' machine_setup/ configs/ tests/ | entr -c make --keep-going check

format:
	@echo ===Formatting code===
	poetry run ruff format $(SRC_DIRECTORIES)
	poetry run ruff check $(SRC_DIRECTORIES) --fix

test:
	@echo ===Tests===
	poetry run pytest -v tests

test_continously:
	fd '\.py$$' $(SRC_DIRECTORIES) | entr -c make test

static_analysis: _type_check _format_check _lint

_format_check:
	@echo ===Checking formatting===
	poetry run ruff format --check $(SRC_DIRECTORIES)

_lint:
	@echo ===Checking linters===
	poetry run ruff check $(SRC_DIRECTORIES)

_type_check:
	@echo ===Checking types===
	poetry run mypy $(SRC_DIRECTORIES)
