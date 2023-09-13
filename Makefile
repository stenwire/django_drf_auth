up:
	@python manage.py runserver

createsuperuser:
	@python manage.py createsuperuser

flush-db:
	@python manage.py flush

format:
	@pipenv run isort . && pipenv run black .

install:
	@pipenv install

shell:
	@pipenv shell

makemigrations:
	@pipenv run python manage.py makemigrations

migrate:
	@pipenv run python manage.py migrate

py-shell:
	@python manage.py shell

test:
	@pipenv run pytest
