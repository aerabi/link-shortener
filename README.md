# Link Shortener Django

## Installation

Create virtualenv and activate it:

```bash
virtualenv -p python3.8 venv
source venv/bin/activate
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

## Create the URL shortener

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
