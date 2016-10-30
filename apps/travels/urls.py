from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<id>\d+)$', views.travels, name = 'login_travels'),
    url(r'^create$', views.create, name = 'travels_create'),
    url(r'^join$', views.join, name = 'travels_join'),
    url(r'^createtravel$', views.createtravel, name = 'travels_createtravel'),
    url(r'^show/(?P<id>\d+)$', views.show, name="travels_show"),
    url(r'^remove/(?P<id>\d+)$', views.remove, name="travels_remove")
]
