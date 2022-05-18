from django.shortcuts import render
from django.http import HttpResponse
import pyshorteners


def index(request):
    return render(request, 'main/index.html')


def shorten_post(request):
    return shorten(request, request.POST['url'])


def shorten(request, url):
    shortener = pyshorteners.Shortener()
    shortened_url = shortener.chilpit.short(url)
    return HttpResponse(f'Shortened URL: <a href="{shortened_url}">{shortened_url}</a>')
