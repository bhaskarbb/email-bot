from rest_framework import serializers

from .models import Meeting
from user.models import Client



class ClientSerializer(serializers.ModelSerializer):

	class Meta:
		model = Client
		fields = ('name', 'email')



class MeetingSerializer(serializers.ModelSerializer):
	client = ClientSerializer(read_only=True)

	class Meta:
		model = Meeting
		fields = ('pk', 'client', 'date', 'start_time', 'end_time', 'busy')
