# Create your views here.
from django.shortcuts import render
from devfest.models import UserAccount, GameInstance

def index(request):
    current_games = GameInstance.objects.filter(users=UserAccount.get(request.user))
    return render(request, 'main/index.html', {
        'current_games' : list(current_games)        
    })