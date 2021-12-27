setup_workstation:
	python3 -m workstation_setup

# the below commands require setting up a virtualenv, activating it, and running `poetry install` in it.

validate_continously:
	fd '\.py$$' workstation_setup/ tests/ | entr -c make lint test

validate: static_checks test

test:
	PYTHONPATH=.:configs/host_agnostic/bin pytest -v tests

static_checks:
	pylint workstation_setup
	isort -c .
