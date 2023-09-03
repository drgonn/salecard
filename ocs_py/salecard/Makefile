
install:
	pip install -r requirements.txt

pkg:
	pip freeze > requirements.txt 

run:
	python manage.py runserver  172.16.114.77:80

migrate:
	python manage.py makemigrations

sqlup:
	python manage.py migrate

redis:
	docker exec -it redis_ocs redis-cli

worker:
	celery -A manage.celery worker --loglevel=info
beat:
	celery -A manage.celery beat --loglevel=info

sql:
	docker exec -it my-postgresql-container psql -U root -d iwp3
