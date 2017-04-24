MANAGE=feedthing/manage.py

noop:
	@echo 'noop'

clean-coverage:
	@if [ -f .coverage ]; then rm .coverage; fi
	@if [ -d htmlcov ]; then rm -r htmlcov; fi

clean-pyc:
	@find . -name '*.pyc' -exec rm {} +

clean-pycache:
	@find . -name '__pycache__' -exec rm -r {} +

makemigrations-all:
	python $(MANAGE) makemigrations

migrate-all:
	python $(MANAGE) migrate

run:
	$(MANAGE) runserver 0.0.0.0:8000

test-all: clean-pyc clean-pycache
	$(MANAGE) test feedthing

test-all-withcoverage: clean-pyc clean-pycache clean-coverage
	coverage run $(MANAGE) test feedthing

,resetdb:
	dropdb feedthing
	createdb feedthing
