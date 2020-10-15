pep8:
	isort app --check-only --skip migrations

fix-import:
	isort app

test:
	pytest -v

coverage:
	pytest -v --cov