pep8:
	isort app --check-only --skip migrations

fix-import:
	isort app
	isort tests

test:
	pytest -v

coverage:
	pytest -v --cov -vv

coverage-report:
	coverage report -m