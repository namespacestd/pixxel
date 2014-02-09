from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from devfest.models import GameInstance, UserAccount, ScoreInstance, DrawInstance
from django.core.files.base import ContentFile
import re
import base64
import hashlib
import time
from datetime import datetime

def public_picture(request, round_number, room_name, player_name):
    target_user = UserAccount.find(player_name)
    target_game = GameInstance.get(room_name)
    draw_instance = DrawInstance.get_for_user_game_round(target_user, target_game, round_number)
    return render(request, "game/public_picture.html", {
        'round_number' : round_number,
        'room_name' : room_name,
        'player_name' : player_name,
        'drawing' : draw_instance
    })