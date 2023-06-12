# The Enchiridion Server
This repository is part of The Enchiridion project, a web application built to assist users in curating and managing custom playlists for TV series episodes using data from The Movie Database (TMDB). The Enchiridion Server is a RESTful API built with Django and Django Rest Framework.

## Features
- Token-based authentication for users
- Endpoints to create, read, update, and delete playlists
- Endpoints to fetch TV series episodes from TMDB
- Endpoints to store and retrieve episodes from local database

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
- Python 3.6+
- Django 4.2+
- Django Rest Framework 3.13.0+

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
4. Add `.env` file in the root directory and insert your TMDB API Key and Django secret key:
```
TMDB_API_KEY = your_tmdb_access_token
SECRET_KEY = your_django_secret_key
```
5. Add `db.sqlite3` file in the root directory and seed it with data via the `seed_db.sh` script:
```
touch db.sqlite3
./seed_db.sh
```
6. Run the server:
```
python manage.py runserver
```

## Technology Stack
- Django
- Django REST Framework
- SQLite
- TMDB API

## Contact
Neil MacLean - nbmac13@gmail.com
