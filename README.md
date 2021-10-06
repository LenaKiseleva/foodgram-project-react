# Foodgram - «Grocery Assistant»
Online service and API. In this service users can publish recipes, subscribe to publications of other users, add favorite recipes to the "Favorites" list, and before going to the store to download a summary list of products needed to prepare one or more selected dishes.

## Tech

Technologies in the project:

- Python 3.8.10 - interpreted, high-level programming language
- Django 3.0.5 - high-level Python web framework
- Gunicorn 20.0.4 - Python WSGI HTTP Server for UNIX
- Docker 20.10.7 - open source containerization platform
- Nginx 1.18.0 - open source software for web serving
- PostgreSQL 12.4 - open-source relational database management system emphasizing extensibility

## Installation
To install docker run the following commands
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh 
```

Follow these steps:
1. Create a folder yamdb
```bash
mkdir foodgram
```
2. Clone this project to this folder
3. Create a .env file with the following content
```bash
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
4. Run docker-compose with the command
```bash
sudo docker-compose up -d
```
5. Make migrations
```bash
sudo docker-compose exec foodgram python manage.py migrate
```
6. Collect statics with the command
```bash
sudo docker-compose exec foodgram python manage.py collectstatic --no-input
```
7. Create superuser
```bash
sudo docker-compose exec foodgram python manage.py createsuperuser --username admin --email 'admin@foodgram.com'
```
Go to http://127.0.0.1/admin/ and make sure the page is fully displayed: the statics are loaded.
Log in as a superuser and make sure the migrations were successful.

## Author:
 - Lena Kiseleva
