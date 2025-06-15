.PHONY: install
install:
	poetry install

.PHONY: runserver
runserver:
	poetry run python manage.py runserver

.PHONY: migrate
migrate:
	poetry run python manage.py migrate

.PHONY: makemigrations
makemigrations:
	poetry run python manage.py makemigrations

.PHONY: superuser
superuser:
	poetry run python manage.py createsuperuser

.PHONY: update
update: install migrate ;

.PHONY: activate
activate:
	source venv/Scripts/activate