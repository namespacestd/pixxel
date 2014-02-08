from django.db import models
from django.contrib.auth.models import User
from django import forms
from operator import itemgetter

class UserAccount(models.Model):
    user = models.ForeignKey(User)
    email_address = models.EmailField()

    @staticmethod
    def get(user):
        # If parameter is empty, return nothing
        if user is None or not user.username:
            return None

        # Check if profile exists, and return it if it does
        results = UserAccount.objects.filter(user=user)
        try:
            return results[0]
        except IndexError:
            return None

    @staticmethod
    def find(username):
        matches = UserAccount.objects.filter(user__username__iexact=username)
        if len(matches):
            return matches[0]
        else:
            return None

    @staticmethod
    def create_new_user(username, email_address, password):
        user = User.objects.create_user(username, email_address, password)
        account = UserAccount()
        account.user = user
        account.email_address = email_address
        account.save()
        return account


class GameInstance(models.Model):
    game_room_name = models.CharField(max_length=50)
    owner = models.ForeignKey(UserAccount, related_name='game_instance_owner')
    users = models.ManyToManyField(UserAccount, related_name='game_instance_user')
    current_judge = models.ForeignKey(UserAccount, related_name='game_instance_judge')
    current_round = models.IntegerField(default=0)
    current_phrase = models.CharField(max_length=50, blank=True)
    is_public = models.BooleanField(default=True)
    password = models.CharField(max_length=50, blank=True)

    @staticmethod
    def get(name):
        # If parameter is empty, return nothing
        if name is None:
            return None

        # Check if profile exists, and return it if it does
        results = GameInstance.objects.filter(game_room_name=name)
        try:
            return results[0]
        except IndexError:
            return None


class ScoreInstance(models.Model):
    user = models.ForeignKey(UserAccount)
    score = models.IntegerField(default=0)
    game = models.ForeignKey(GameInstance)
    seen_previous_result = models.BooleanField(default=True)

    @staticmethod
    def get(user, game):
        # If parameter is empty, return nothing
        if user is None or game is None:
            return None

        # Check if profile exists, and return it if it does
        results = ScoreInstance.objects.filter(user=user, game=game)
        try:
            return results[0]
        except IndexError:
            return None

    @staticmethod
    def get_all_for_game(game):
        if game is None:
            return None

        results = ScoreInstance.objects.filter(game=game)
        return results

class DrawInstance(models.Model):
    user = models.ForeignKey(UserAccount, related_name='draw_instance_user')
    picture = models.ImageField(upload_to="static/img/user_pictures/")
    game = models.ForeignKey(GameInstance)
    round_number = models.IntegerField()
    was_round_winner = models.BooleanField(default=False)
    round_judge = models.ForeignKey(UserAccount,related_name='draw_instance_judge')
    phrase = models.CharField(max_length=50)

    @staticmethod
    def get(user, game, round_number):
        # If parameter is empty, return nothing
        if user is None or game is None or round_number is None:
            return None

        # Check if profile exists, and return it if it does
        results = DrawInstance.objects.filter(user=user, game=game, round_number=round_number)
        try:
            return results[0]

        except IndexError:
            return None

    @staticmethod
    def get_recent_images(user):
        if user is None:
            return None

        #Check if user has images, and return them
        results = DrawInstance.objects.filter(user=user)
        try:
            user_images = []
            for instance in results:
                picture_data = {}
                picture_data["picture"] = instance.picture
                picture_data["was_round_winner"] = instance.was_round_winner
                picture_data["phrase"] = instance.phrase
                picture_data["timestamp"] = instance.timestamp
                user_images.append(picture_data)
            recent_images = sorted(l, key=itemgetter('timestamp'), reverse=True)
            del recent_images[5:]
        return recent_images

        except IndexError:
            return None 

    @staticmethod
    def get_all_for_round(game, round_number):
        if game is None or round_number is None:
            return None
            
        results = DrawInstance.objects.filter(game=game, round_number=round_number)
        return results


class CreateAccountForm(forms.Form):
    """
    Account creation form, including username, password and email address.
    """
    email_address = forms.CharField(label="Email address")  # TODO: change to regexfield
    username = forms.RegexField(
        label="Username",
        max_length=30,
        regex=r'^[\w-]{6,30}$',
        help_text="Required. Between 6 and 30 characters. Letters, digits and -/_ only.",
        error_messages={'invalid': "This value may contain only letters, \
                                    numbers and -/_ characters, and must \
                                    be between 6 and 30 characters long."})
    password1 = forms.CharField(
        label="Password",
        min_length=6,
        max_length=30,
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation",
        min_length=6,
        max_length=30,
        widget=forms.PasswordInput,
        help_text="Enter the same password as above, for verification.")

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            if UserAccount.find(username=username):
                logger.info("Found duplicate username in database.")
            else:
                User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("A user with that username already exists.")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2

    def save(self):
        password = self.cleaned_data.get("password1")
        email_address = self.cleaned_data.get("email_address")
        username = self.cleaned_data.get('username')
        return UserAccount.create_new_user(username, email_address, password)


