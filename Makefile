.DEFAULT_GOAL := ,noop
.PHONY: docs

MANAGE=feedthing/manage.py
HOST=0.0.0.0
PORT=8000

clean-coverage:
	@if [ -f .coverage ]; then rm .coverage; fi
	@if [ -d htmlcov ]; then rm -r htmlcov; fi

clean-pyc:
	@find . -name '*.pyc' -exec rm {} +

clean-pycache:
	@find . -name '__pycache__' -exec rm -r {} +

coverage-html:
	@coverage html

coverage-html-browser: coverage-html
	python -m webbrowser -t file://$(PWD)/htmlcov/index.html

createuser:
	$(MANAGE) createuser $(email)

docs:
	cd docs && make html

makemigrations-all:
	$(MANAGE) makemigrations

migrate-all:
	$(MANAGE) migrate

run:
	$(MANAGE) runserver $(HOST):$(PORT)

test-all: clean-pyc clean-pycache
	$(MANAGE) test feedthing --settings=config.settings.tests

test-all-withcoverage: clean-pyc clean-pycache clean-coverage
	coverage run $(MANAGE) test feedthing --settings=config.settings.tests

test-app: clean-pyc clean-pycache
	$(MANAGE) test $(app) --settings=config.settings.tests

test-app-withcoverage: clean-pyc clean-pycache clean-coverage
	coverage run --source=$(app) $(MANAGE) test $(app) --settings=config.settings.tests

test-all-failfast: clean-pyc clean-pycache
	$(MANAGE) test feedthing --settings=config.settings.tests --failfast

test: test-all

test-failfast: test-all-failfast

,noop:
	@echo noop
