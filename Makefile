.DEFAULT_GOAL := ,noop
.PHONY: clean-coverage clean-pyc clean-pycache coverage-html \
		coverage-html-browser makemigrations-all migrate-all run \
		test-all test-all-withcoverage ,noop ,resetdb

HOST=0.0.0.0
MANAGE=feedthing/manage.py
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

makemigrations-all:
	$(MANAGE) makemigrations

migrate-all:
	$(MANAGE) migrate

run:
	$(MANAGE) runserver $(HOST):$(PORT)

test-all: clean-pyc clean-pycache
	$(MANAGE) test feedthing

test-all-withcoverage: clean-pyc clean-pycache clean-coverage
	coverage run $(MANAGE) test feedthing

,noop:
	@echo 'noop'

,resetdb:
	dropdb feedthing
	createdb feedthing
