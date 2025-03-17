import uuid
from django.db import models
from django.contrib.auth.models import User

class Word(models.Model):
    """Model to store words for the game"""
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    word = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.word

class Game(models.Model):
    """Model to store game sessions"""
    session = models.CharField(max_length=255, unique=True)
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="games")
    letter_knows = models.CharField(max_length=50, default="", blank=True)
    fault = models.IntegerField(default=0)
    win = models.BooleanField(default=False)

    def __str__(self):
        return f"Game {self.id} - {self.word.word} ({'Won' if self.win else 'Ongoing'})"

class Profile(models.Model):
    """Model to store user profiles"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_image = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    def __str__(self):
        return self.user.username
