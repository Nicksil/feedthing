COVERAGEHTMLINDEX=./htmlcov/index.html
MANAGE=./feedthing/manage.py
PYTHON=python3

,resetdb:
	dropdb feedthing
	createdb feedthing

cleancoverage:
	@if [ -f .coverage ]; then rm .coverage; fi
	@if [ -d htmlcov ]; then rm -r htmlcov; fi

makemigrations:
	python $(MANAGE) makemigrations

migrate:
	python $(MANAGE) migrate

run:
	$(MANAGE) runserver 0.0.0.0:8000

test:
	$(MANAGE) test

llama:
	@echo $(1)

testwithcoverage:
	coverage run $(MANAGE) test feedthing
	coverage html
	@$(PYTHON) -m webbrowser -t file://$(PWD)/htmlcov/index.html
