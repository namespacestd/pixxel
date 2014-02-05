from django.conf.urls import patterns, url
from game import views

urlpatterns = patterns('',
    url(r'^new_game/', views.new_game, name='new_game'),
    url(r'^open_games/', views.open_games, name='open_games'),
    url(r'^create_new_room', views.create_new_room, name='create_new_room'),
    url(r'^room/(?P<room_name>\w+)/+$', views.game_room, name='game_room'),
    url(r'^room/join_game/(?P<room_name>\w+)/+$', views.join_game, name='join_game'),
    url(r'^submit_drawing/(?P<room_name>\w+)/+$', views.submit_drawing, name='submit_drawing'),
)