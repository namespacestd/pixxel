from django.db import models
from django.contrib.auth.models import User

class UserAccount(models.Model):
    user = models.ForeignKey(User)

class GameInstance(models.Model):
    users = models.ManyToManyField(UserAccount, related_name='game_instance_user')
    current_judge = models.ForeignKey(UserAccount, related_name='game_instance_judge')

class ScoreInstance(models.Model):
    user = models.ForeignKey(UserAccount)
    score = models.IntegerField(default=0)
    game = models.ForeignKey(GameInstance)