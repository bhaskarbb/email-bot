from django.shortcuts import HttpResponse

from .models import User
import json


def login(request):
    if request.method == 'POST':
        user_json = request.POST.get('kuch_bhi')

        token = '1'
        if not User.objects.filter(token=token).exists():
            user = User(email='xbox2752@gmail.com', first_name=name)
            user.save()
            return HttpResponse('Logged in')
    else:
        return HttpResponse('You must login first')



def schedule_client_meeting(data):

	parameter = data['result']['parameters']
	date = parameter['date']
	start_time = parameter['time']
	end_time = calc_end_time(start_time)
	name = parameter['name']
	email = parameter['email']

	if check_meeting_conflict(date, start_time, end_time):
		message = message_generator('meeting-conflict')

	elif name:
		client = Client.objects.filter(name__icontains=name).first()
		if client.exists():
			Meeting.objects.create(user_id=1,  client=client, date=date, start_time=start_time, end_time=end_time, busy=False)
			message = message_generator('meeting-confirm')

		else:
			messsage = message_generator('name-not-found')


	elif email:
		client = Client.objects.filter(email=email).first()
		if not client.exists():
			client = Client.objects.create(name=email, email=email)

		Meeting.objects.create(user_id=1,  client=client, date=date, start_time=start_time, end_time=end_time, busy=False)
		message = message_generator('meeting-confirm')

	else:
		messsage = message_generator('invalid')

	response = generate_response(message)
	return JsonResponse(response)



def add_client(data):
	parameter = data['result']['parameters']
	name = parameter['name']
	email = parameter['email']

	Client.objects.create(name=name, email=email)
	messsage = 'Client has been added'
	
	response = generate_response(message)
	return JsonResponse(response)