from django.shortcuts import render
from devfest.models import GameInstance

def new_game(request):
    return render(request, 'game/game.html')

def create_new_room(request):
    if request.method == 'POST':
        game_name = request.POST['room_name']

        new_game = GameInstance(game_room_name=game_name)
        new_game.save()
    
    return render(request, 'game/game.html')