from django.db import models
from user.models import User, Client


class Meeting(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
	date = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField()
	timestamp = models.DateTimeField(auto_now=True)
	busy = models.BooleanField(default=False)

	def __str__(self):
		return '{} : {} to {}'.format(self.date, self.start_time, self.end_time)

