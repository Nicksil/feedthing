MANAGE=./feedthing/manage.py

run:
	MANAGE runserver 0.0.0.0:8000

,resetdb:
	dropdb feedthing
	createdb feedthing

makemigrations:
	python MANAGE makemigrations

migrate:
	python MANAGE migrate
