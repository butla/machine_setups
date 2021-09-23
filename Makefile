setup_workstation:
	python3 -m workstation_setup


# the below commands require setting up a virtualenv, activating it, and running `poetry install` in it.
test:
	PYTHONPATH=.:configs/host_agnostic/bin pytest -v tests

test_continously:
	fd '\.py$$' workstation_setup/ tests/ | entr -c make test
