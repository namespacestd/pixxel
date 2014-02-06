from django.shortcuts import render, HttpResponseRedirect
from devfest.models import GameInstance, UserAccount, ScoreInstance, DrawInstance

def new_game(request):
    return render(request, 'game/game.html')

def create_new_room(request):
    if request.method == 'POST':
        game_name = request.POST['room_name']
        is_private = request.POST.get('is_private')
        
        if GameInstance.get(game_name):
            return render(request, 'game/game.html', { 'error' : 'already exists' })

        new_game = GameInstance()
        new_game.game_room_name = game_name
        current_user = UserAccount.get(request.user)
        new_game.current_judge = current_user
        new_game.owner = current_user

        if is_private:
            new_game.is_public = False
            new_game.password = request.POST['room_password']

        new_game.save()
        join_game_helper(current_user, game_name)
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
    current_judge = None
    user_drawing = None
    num_submitted = 0

    previous_result_data = None

    if request.user:
        already_in_game = UserAccount.get(request.user) in userlist

    user_scores = []
    user_drawings = []

    for user in userlist:
        score = ScoreInstance.get(user, current_room)
        user_scores.append(({'username' : user.user.username, 'score': score})) 
        
        if user.user == request.user and user == current_room.current_judge:
            current_judge = user

        if user.user == request.user and score.seen_previous_result == False:
            last_round_number = current_room.current_round-1
            drawings = DrawInstance.get_all_for_round(current_room, last_round_number)

            previous_result_data = drawings

    for user in userlist:
        if user != current_room.current_judge:
            drawing = DrawInstance.get(user, current_room, current_room.current_round)
            user_drawings.append({'username': user.user.username, 'drawing': drawing})

            if request.user == user.user and drawing != None:
                user_drawing = drawing
            if drawing != None:
                num_submitted+=1

    return render(request, 'game/game_room.html', { 
        'game_instance' : current_room,
        'room_name' : room_name, 
        'userlist' : user_scores,
        'num_drawing' : len(userlist)-1,
        'user_drawings' :  user_drawings,
        'already_in_game' : already_in_game,
        'is_current_judge' : current_judge,
        'user_drawing' : user_drawing,
        'all_submitted' : num_submitted == len(userlist)-1,
        'previous_round_data' : previous_result_data
    })

def join_game(request, room_name):
    join_game_helper(UserAccount.get(request.user), room_name)
    return HttpResponseRedirect('/game/room/' + room_name)

def join_game_helper(user_account, room_name):
    current_user = user_account
    current_room = GameInstance.get(room_name)
    already_in_game = user_account in current_room.users.all()

    if not already_in_game:
        current_room.users.add(current_user)

    user_score = ScoreInstance(user=current_user, score=0, game=current_room)
    user_score.save()

def submit_drawing(request, room_name):
    current_user = UserAccount.get(request.user)
    current_room = GameInstance.get(room_name)
    round_number = current_room.current_round
    user_drawing = request.FILES['drawn_image']

    drawing = DrawInstance(user = current_user, picture=user_drawing, game=current_room, round_number=round_number, round_judge=current_room.current_judge)
    drawing.save()
    
    return HttpResponseRedirect('/game/room/' + room_name)

def judge_drawing(request, room_name):
    if request.method == 'POST':
        chosen_drawing = None
        for key, value in request.POST.items():
            if value == 'Choose this Drawing':
                chosen_drawing = UserAccount.find(key)

        game_room = GameInstance.get(room_name)
        user_scores = ScoreInstance.get_all_for_game(game_room)
        draw_instance = DrawInstance.get(chosen_drawing, game_room, game_room.current_round)

        for user in user_scores:
            user.seen_previous_result = False
            user.save()

        game_room.current_round+=1
        game_room.save()
        draw_instance.was_round_winner = True
        draw_instance.save()

        choose_next_judge(game_room)

    return HttpResponseRedirect('/game/room/' + room_name)

def next_round(request, room_name):
    current_user = UserAccount.get(request.user)
    current_room = GameInstance.get(room_name)

    score = ScoreInstance.get(current_user, current_room)
    score.seen_previous_result = True
    score.save()
    return HttpResponseRedirect('/game/room/' + room_name)

def choose_next_judge(game_instance):
    current_judge = game_instance.current_judge
    next_judge = game_instance.users.all()[0]
    found_current = False

    for user in game_instance.users.all():
        if found_current:
            next_judge = user
            found_current = False
            break
        if user == current_judge:
            found_current = True

    game_instance.current_judge = next_judge
    print next_judge.user.username
    game_instance.save()



