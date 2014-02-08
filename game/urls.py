from django.conf.urls import patterns, url
from game import views

urlpatterns = patterns('',
    url(r'^new_game/', views.new_game, name='new_game'),
    url(r'^open_games/', views.open_games, name='open_games'),
    url(r'^create_new_room', views.create_new_room, name='create_new_room'),
    url(r'^room/(?P<room_name>[\w|\W]+)/+$', views.game_room, name='game_room'),
    url(r'^room/join_game/(?P<room_name>[\w|\W]+)/+$', views.join_game, name='join_game'),
    url(r'^submit_drawing/(?P<room_name>[\w|\W]+)/+$', views.submit_drawing, name='submit_drawing'),
    url(r'^judge_phrase/(?P<room_name>[\w|\W]+)/+$', views.judge_phrase, name='judge_phrase'),
    url(r'^judge_drawing/(?P<room_name>[\w|\W]+)/+$', views.judge_drawing, name='judge_drawing'),
    url(r'^next_round/(?P<room_name>[\w|\W]+)/+$', views.next_round, name='next_round'),
    url(r'^leave_room/(?P<room_name>[\w|\W]+)/+$', views.leave_room, name='leave_room'),
    url(r'^start_game/(?P<room_name>[\w|\W]+)/+$', views.start_game, name='start_game'),
    url(r'^room/kick_player/(?P<room_name>[\w|\W]+)/+$', views.kick_player, name='kick_player'),
)
