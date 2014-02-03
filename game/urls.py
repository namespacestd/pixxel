from django.conf.urls import patterns, url
from game import views

urlpatterns = patterns('',
    url(r'^new_game/', views.new_game, name='new_game'),
    url(r'^create_new_room', views.create_new_room, name='create_new_room')
)