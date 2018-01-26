from django.db import models

# Create your models here.


class Client(models.Model):
	name = models.CharField(max_length=60)
	email = models.EmailField()

	def __str__(self):
		return self.name


class Meeting(models.Model):
	client = models.ForeignKey(Client, on_delete=models.CASCADE)
	time = models.DateTimeField()

	def __str__(self):
		return '{} : {}'.format(self.client, self.time)



