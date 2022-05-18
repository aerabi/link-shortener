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

## Create the Form