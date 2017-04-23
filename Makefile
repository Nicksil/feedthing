MANAGE=./feedthing/manage.py

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

testwithcoverage:
	coverage run $(MANAGE) test
