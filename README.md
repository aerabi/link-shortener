# Link Shortener Django

## Table of Contents

* [Installation](#installation)
* [Create the Project from the Scratch](#create-the-project-from-the-scratch)
  + [Create the URL Shortener](#create-the-url-shortener)
  + [Create the Form](#create-the-form)
  + [Add Docker Compose](#add-docker-compose)

## Installation

Create virtualenv and activate it:

```bash
virtualenv -p python3.8 venv
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Create the Project from the Scratch

Create virtualenv and activate it:

```bash
virtualenv -p python3.8 venv
source venv/bin/activate
```

Install Django:

```bash
pip install Django
```

Create a `src` directory and go there:

```bash
mkdir -p src && cd src
```

Create a Django project there:

```bash
django-admin startproject urlshortener
```

By creating the Django project, the tree structure of the repo
would look like this:

```
src
└── urlshortener
    ├── manage.py
    └── urlshortener
        ├── asgi.py
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py

```

Now, let's create the Django app for shortening the URLs:

```bash
cd src/urlshortener
python manage.py startapp main
```

It will create directory under `src/urlshortener`:

```
src
└── urlshortener
    ├── main
    │   ├── admin.py
    │   ├── apps.py
    │   ├── __init__.py
    │   ├── migrations
    │   ├── models.py
    │   ├── tests.py
    │   └── views.py
    ├── manage.py
    └── urlshortener
```

### Create the URL Shortener

Install the package `urlshorteners`:

```bash
pip install pyshorteners
```

Dump the pip freeze for the next generations:

```bash
pip freeze > requirements.txt
```

Head to `main/views.py` and edit it accordingly:

```python
from django.shortcuts import render
from django.http import HttpResponse
import pyshorteners


# Create your views here.
def shorten(request, url):
    shortener = pyshorteners.Shortener()
    shortened_url = shortener.chilpit.short(url)
    return HttpResponse(f'Shortened URL: <a href="{shortened_url}">{shortened_url}</a>')

```

Now, we should assign a URL to this function. Create a `urls.py` under `main`:

```bash
touch main/urls.py
```

And fill it up:

```python
from django.urls import path

from . import views

urlpatterns = [
    path('shorten/<str:url>', views.shorten, name='shorten'),
]
```

Now head back to the `urlshortener/urls.py` and include the newly created `urls.py` file:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
]
```

Now, run the development server:

```bash
python manage.py runserver
```

And open [`127.0.0.1:8000/shorten/aerabi.com`](http://127.0.0.1:8000/shorten/aerabi.com)
in your browser.

### Create the Form

Now let's create the landing page. Create a new HTML file:

```bash
mkdir -p main/templates/main
touch main/templates/main/index.html
```

Open the `index.html` and fill it up the with following content:

```html
<form action="{% url 'main:shorten' url %}" method="post">
{% csrf_token %}
<fieldset>
    <input type="text" name="url">
</fieldset>
<input type="submit" value="Shorten">
</form>
```

Now head to `main/views.py` and create two functions, namely `index` and `shorten_post`:

```python
from django.shortcuts import render
from django.http import HttpResponse
import pyshorteners


def index(request):
    return render(request, 'main/index.html')


def shorten_post(request):
    return shorten(request, request.POST['url'])


. . .
```

Then to the `main/urls.py` to bind the function to URLs:

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shorten', views.shorten_post, name='shorten_post'),
    path('shorten/<str:url>', views.shorten, name='shorten'),
]
```

The main difference between `shorten` and `shorten_post` is that the latter accepts
HTTP POST parameters instead of URL path parameters.

Now head to `urlshortener/settings.py` and add `'main.apps.MainConfig'` to the beginning of the list `INSTALLED_APPS`:

```python
. . .

INSTALLED_APPS = [
    'main.apps.MainConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

. . .
```

Now restart the development server:

```bash
python manage.py runserver
```

This time go to the root: [`127.0.0.1:8000`](http://127.0.0.1:8000/)

Bingo!

### Add Docker Compose

To use Docker Compose with the current setup, first add Gunicorn to the list of dependencies:

```
gunicorn==20.1.0
psycopg2-binary==2.9.3
```

Now, create the following `docker-compose.yml` file in the root of the repo:

```yml
version: '3.2'

services:
  web:
    build: ./src/urlshortener/
    command: gunicorn urlshortener.wsgi:application --bind 0.0.0.0:8000
    ports:
      - 8000:8000
```

Now, start the app using Docker Compose:

```bash
docker-compose build
docker-compose up -d
```

The server should run on port 8000 now: [`127.0.0.1:8000`](http://127.0.0.1:8000/)

### Create Database Models

Now, to save the URLs and their short versions locally, we should create database models for them.
Head to `main/models.py` and created the following model:

```python
from django.db import models


# Create your models here.
class Question(models.Model):
    original_url = models.CharField(max_length=256)
    hash = models.CharField(max_length=10)
    creation_date = models.DateTimeField('creation date')

```

We'll assume that the given URLs fit in 256 characters and the short version are less than 10 characters
(usually 7 characters would suffice).

Now, create the database migrations:

```
python manage.py makemigrations
```

A new file will be created under `main/migrations`. Commit this file.

Now to apply the database migrations to the default SQLite DB, run:

```bash
python manage.py migrate
```

Now that we have the database models, we would want to create a shortener service.
Create a Python file `main/service.py` and add the following functionality:

```python
import random
import string
from django.utils import timezone

from .models import LinkMapping


def shorten(url):
    random_hash = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(7))
    mapping = LinkMapping(original_url=url, hash=random_hash, creation_date=timezone.now())
    mapping.save()
    return random_hash


def load_url(url_hash):
    return LinkMapping.objects.get(hash=url_hash)

```

Now, create a new function in the views for redirecting:

```python
from django.shortcuts import render, redirect

from . import service

. . .

def redirect_hash(request, url_hash):
    original_url = service.load_url(url_hash).original_url
    return redirect(original_url)
```

Create a URL mapping for the redirect function:

```python
urlpatterns = [
    path('', views.index, name='index'),
    path('shorten', views.shorten_post, name='shorten_post'),
    path('shorten/<str:url>', views.shorten, name='shorten'),
    path('<str:url_hash>', views.redirect_hash, name='redirect'),
]
```

And finally change the shorten view function to use the internal service:

```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from . import service

. . .

def shorten(request, url):
    shortened_url_hash = service.shorten(url)
    shortened_url = request.build_absolute_uri(reverse('redirect', args=[shortened_url_hash]))
    return HttpResponse(f'Shortened URL: <a href="{shortened_url}">{shortened_url}</a>')
```

We can also remove the third-party shortener library from `requirements.txt`, as we don't use it anymore.

### Use PostgreSQL

To use PostgreSQL instead of SQLite, we'll change the config in `settings.py`:

```python
import os

. . .

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if os.environ.get('POSTGRES_NAME'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_NAME'),
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': 'db',
            'PORT': 5432,
        }
    }
```

Now head to `docker-compose.yml` and change it to the following:

```yaml
version: '3.2'

services:
  web:
    build: ./src/urlshortener/
    command: gunicorn urlshortener.wsgi:application --bind 0.0.0.0:8000
    ports:
      - 8000:8000
    environment:
      - POSTGRES_NAME=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    depends_on:
      - db
  db:
    image: postgres
    volumes:
      - ./data/db:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
```

Now start the Docker Compose services:

```bash
docker-compose up --build -d
```

Now, to do the migrations, do:

```bash
docker-compose exec web python manage.py migrate
```

The web server is not ready. Go ahead and try it: [`127.0.0.1:8000`](http://127.0.0.1:8000/)

### Make it Pretty

Create a `base.html` under `main/templates/main`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Link Shortener</title>
  <link href="https://unpkg.com/material-components-web@latest/dist/material-components-web.min.css" rel="stylesheet">
  <script src="https://unpkg.com/material-components-web@latest/dist/material-components-web.min.js"></script>
</head>
<style>
  #main-card {
      margin:0 auto;
      display: flex;
      width: 50em;
      align-items: center;
  }
</style>
<body class="mdc-typography">
<div id="main-card">
  {% block content %}
  {% endblock %}
</div>
</body>
```

Alter the `index.html` to use material design:

```html
{% extends 'main/base.html' %}

{% block content %}
<form action="{% url 'shorten_post' %}" method="post">
  {% csrf_token %}
  <label class="mdc-text-field mdc-text-field--outlined">
      <span class="mdc-notched-outline">
        <span class="mdc-notched-outline__leading"></span>
        <span class="mdc-notched-outline__notch">
          <span class="mdc-floating-label" id="my-label-id">URL</span>
        </span>
        <span class="mdc-notched-outline__trailing"></span>
      </span>
    <input type="text" name="url" class="mdc-text-field__input" aria-labelledby="my-label-id">
  </label>
  <button class="mdc-button mdc-button--outlined" type="submit">
    <span class="mdc-button__ripple"></span>
    <span class="mdc-button__label">Shorten</span>
  </button>
</form>
{% endblock %}
```

Create another view for the response, namely `link.html`:

```html
{% extends 'main/base.html' %}

{% block content %}
<div class="mdc-card__content">
  <p>Shortened URL: <a href="{{shortened_url}}">{{shortened_url}}</a></p>
</div>
{% endblock %}
```

Now, get back to `views.py` and change the `shorten` function to render instead of
returning a plain HTML:

```python
. . .

def shorten(request, url):
    shortened_url_hash = service.shorten(url)
    shortened_url = request.build_absolute_uri(reverse('redirect', args=[shortened_url_hash]))
    return render(request, 'main/link.html', {'shortened_url': shortened_url})
```

To apply the changes, do:

```bash
docker-compose up --build -d
```