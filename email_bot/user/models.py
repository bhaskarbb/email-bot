from django.db import models
from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     token = models.CharField(max_length=1024)

class User(models.Model):
	name = models.CharField(max_length=128)
	email = models.EmailField(unique=True)

	def __str__(self):
		return self.name


class Client(models.Model):
	name = models.CharField(max_length=128)
	email = models.EmailField(unique=True)

	def __str__(self):
		return self.name


class Schedule(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	day = models.IntegerField()
	start_time = models.TimeField(default='08:00:00')
	end_time = models.TimeField(default='16:00:00')
	busy_day = models.BooleanField(default=False)

	def __str__(self):
		return str(self.day)

