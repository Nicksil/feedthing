MANAGE=./feedthing/manage.py

,resetdb:
	dropdb feedthing
	createdb feedthing

makemigrations:
	python $(MANAGE) makemigrations

migrate:
	python $(MANAGE) migrate

run:
	$(MANAGE) runserver 0.0.0.0:8000
