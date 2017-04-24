MANAGE=./feedthing/manage.py

noop:
	@echo 'noop'

clean-coverage:
	@if [ -f .coverage ]; then rm .coverage; fi
	@if [ -d htmlcov ]; then rm -r htmlcov; fi

makemigrations-all:
	python $(MANAGE) makemigrations

migrate-all:
	python $(MANAGE) migrate

run:
	$(MANAGE) runserver 0.0.0.0:8000

test-all:
	$(MANAGE) test

test-all-withcoverage:
	coverage run $(MANAGE) test feedthing

,resetdb:
	dropdb feedthing
	createdb feedthing
