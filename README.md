# The Enchiridion Server

This repository is part of The Enchiridion project, a web application built to assist users in curating and managing custom playlists for TV series episodes using data from The Movie Database (TMDB). The Enchiridion Server is a RESTful API built with Django and Django Rest Framework.

## Features

- Custom cookie-based authentication for users
- Endpoints to create, read, update, and delete playlists
- Endpoints to fetch TV series episodes from TMDB
- Endpoints to store and retrieve episodes from local database
- Full testing suite including unit tests for all models and serializers, and integration testing for all views

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.9+
- Django 4.2+
- Django Rest Framework 3.13.0+
- PostgreSQL 14.1+

### Installation and Setup

1. Clone this repository:
```
git clone git@github.com:macleann/enchiridion-server.git
```
2. Move to the directory:
```
cd enchiridion-server
```
3. Create a virtual environment and install the requirements:
```
pipenv shell
pipenv install
```
4. Create a local PostgreSQL database. I followed [the documentation](https://www.postgresql.org/docs/current/tutorial-start.html). For the prod database, I opted to use [tembo.io](https://tembo.io/docs/).
5. Add a `.env` file in the root directory and insert the following requisite keys (be sure to use the proper DB values from the prior step):
```
TMDB_API_KEY=your_tmdb_access_token
SECRET_KEY=your_django_secret_key
MY_SECRET_KEY=your_secret_key
ALLOWED_HOST=localhost # `enchiridion.tv` in production
CLIENT_URL=http://localhost:3000 # `http://enchiridion.tv` in production
WWW_CLIENT_URL=http://www.localhost:3000 # `http://www.enchiridion.tv` in production
DEBUG=True # False in production
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
DB_ENGINE=django.db.backends.postgresql # don't change this!
DB_NAME=your_db_name
DB_USER=your_postgres_user # probably `postgres`
DB_PASSWORD=your_password
DB_HOST=localhost # for tembo.io users, this should look like `your-org-inst-your-db-name.data-1.use1.tembo.io`
DB_PORT=5432
```
6. Make and run migrations:
```
python manage.py makemigrations
python manage.py migrate
```
7. Seed the database (don't forget to make the script executable):
```
./seed_db.sh
```
8. Run the server:
```
python manage.py runserver
```

## Technology Stack

- Django
- Django REST Framework
- Simple JWT
- PostgreSQL
- TMDB API

## Contact

Neil MacLean - nbmac13@gmail.com