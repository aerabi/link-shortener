from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shorten', views.shorten_post, name='shorten_post'),
    path('shorten/<str:url>', views.shorten, name='shorten'),
    path('<str:url_hash>', views.redirect_hash, name='redirect'),
]
