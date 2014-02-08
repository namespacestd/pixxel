# Create your views here.
from django.shortcuts import render
from devfest.models import UserAccount, GameInstance

def index(request):
    user_games = GameInstance.objects.filter(users=UserAccount.get(request.user))
    current_games = []
    completed_games = []

    for current_room in user_games:
        if current_room.current_round >= current_room.num_rounds:
            completed_games.append(current_room)
        else:
            current_games.append(current_room)

    return render(request, 'main/index.html', {
        'current_games' : list(current_games),
        'completed_games' : list(completed_games),  
    })