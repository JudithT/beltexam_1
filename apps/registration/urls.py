from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^quotes$', views.quotes),
    url(r'^login$', views.login),
    url(r'^process$', views.process),
    url(r'^users/(?P<id>\d+)$', views.users),
    url(r'^logout$', views.logout),
    url(r'^createfavorite$', views.createfavorite),
    url(r'^removefavorite$', views.removefavorite)








    # url(r'^hello$', views.hello),

]
