from django.shortcuts import render
from devfest.models import GameInstance, UserAccount

def new_game(request):
    return render(request, 'game/game.html')

def create_new_room(request):
    if request.method == 'POST':
        game_name = request.POST['room_name']
        
        if GameInstance.get(game_name):
            return render(request, 'game/game.html', { 'error' : 'already exists' })
            
        new_game = GameInstance()
        new_game.game_room_name = game_name
        current_user = UserAccount.get(request.user)
        new_game.current_judge = current_user
        new_game.save()
        new_game.users.add(current_user)

    
    return render(request, 'game/game.html')