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

## Create the Form

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

Now head to `urlshortener/settings.py` and add `'main'` to the end of the list `INSTALLED_APPS`:

```python
. . .

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
]

. . .
```

Now restart the development server:

```bash
python manage.py runserver
```

This time go to the root: [`127.0.0.1:8000`](http://127.0.0.1:8000/)

Bingo!