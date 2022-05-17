# Movie Database REST API
## _Movie database using https://www.omdbapi.com_


Movie Database REST API is a small app created to pass an online test. It allows fetching movies data from an external API database (https://www.omdbapi.com) and inserting them to a local database.

- It is written with Python/Django and uses SQLite as a database engine. 
- Some additional modules were added to allow RESTful operations (Django Rest Framework) and filtering (Django Filter).

## Installation

This app requires Python 3.10 and Django 4.0 for to work properly.

Pip is also required to install dependencies.

Clone the repository.

```sh
git clone https://github.com/medbouya/movie-rest-api.git
```
Install the Django dependencies .
```sh
cd movie-rest-api
pip install -r requirements.txt
```

Run the app...

```sh
python manage.py runserver
```
...and visit http://localhost:8000 

## Instructions for common oprations
You can access the movies list by going to: http://localhost:8000/api/movies. This same URL allows you to add new entries to the database. You can filter movies by year by clicking on the filters button at the top right.

To access comments, go to the following link: http://localhost:8000/api/comments. You can add new comments on the same link. In order to filter comments by movie, append the movie id to the comments URL (i.e. http://localhost:8000/api/comments/1) or use the filter button directly in the top right corner.

## Unit tests
`test.py` in movies/ folder contains all unit tests. 