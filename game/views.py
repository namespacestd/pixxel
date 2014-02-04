from django.shortcuts import render, HttpResponseRedirect
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
        return HttpResponseRedirect('/game/room/'+game_name)
    
    return render(request, 'game/game.html')

def open_games(request):
    open_games = GameInstance.objects.all()
    return render(request, 'game/open_games.html', {
        'open_games': open_games
    })

def game_room(request, room_name):
    current_room = GameInstance.get(room_name)
    userlist = current_room.users.all()
    already_in_game = None

    if request.user:
        already_in_game = UserAccount.get(request.user) in userlist

    return render(request, 'game/game_room.html', { 
        'room_name' : room_name, 
        'userlist' : current_room.users.all(),
        'already_in_game' : already_in_game
    })

def join_game(request, room_name):
    current_user = UserAccount.get(request.user)
    current_room = GameInstance.get(room_name)
    already_in_game = UserAccount.get(request.user) in current_room.users.all()

    if not already_in_game:
        current_room.users.add(current_user)

    return HttpResponseRedirect('/game/room/'+room_name)    