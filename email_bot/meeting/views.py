from django.shortcuts import HttpResponse
from django.http import JsonResponse

#rest framework
from rest_framework.views import APIView
from rest_framework.response import Response

#models and views
from .models import Meeting
from user.models import Schedule, Client
from .serializers import MeetingSerializer

from datetime import datetime, timedelta
import random
import json


class GetMeeting(APIView):

	def get(self, request):		
		timestamp = request.GET.get('timestamp')
		# ajax request - send only new meeting objects
		if timestamp:
			meetings = Meeting.objects.filter(timestamp__gt=timestamp)
		# page load/refresh request - send all meeting objects
		else:
			meetings = Meeting.objects.all()

		meeting_serializer = MeetingSerializer(meetings, many=True)
		return Response(meeting_serializer.data)

	def post(self, request):
		pass



############ SCHEDULE MEETING ###################

# schedules meetings based on avaibility
def schedule_meeting(data):
	parameter = data['result']['parameters']
	date = parameter['date']

	start_time = parameter['time']
	end_time = calc_end_time(start_time)

	client_email = data['result']['resolvedQuery'].split('<')[1].split('>')[0]

	# if meeting time has expired
	if has_meeting_lapsed(date, start_time):
		message = message_generator('lapsed')

	# if meeting isn't on valid date and time or if the meetings conflicts with other meeting
	elif check_schedule_conflict(date, start_time, end_time) or check_meeting_conflict(date, start_time, end_time):
		message =  message_generator('no-meeting')

	else:
		add_meeting(date, client_email, start_time, end_time)
		message =  message_generator('meeting').format(date, start_time)

	# add salutations
	message = '{},\n\n{}\n\n{}'.format(message_generator('open-salutation'), message, message_generator('close-salutation'))

	response = generate_response(message)
	return JsonResponse(response)
	

# calculates end time of meeting with default duration = 2hrs
def calc_end_time(start_time):
	duration = 2 #in hrs
	time_format = '%H:%M:%S'
	end_time = datetime.strptime(start_time, time_format) + timedelta(hours=duration)
	return end_time.strftime(time_format)


# meeting has to be booked 2 hrs before meeting start time
def has_meeting_lapsed(date, start_time):
	datetime_format = '%H:%M:%S%Y-%m-%d'
	meeting_datetime = datetime.strptime(start_time + date, datetime_format)

	# check if meeting happens atleast 2 hrs after booking
	if meeting_datetime > datetime.now() + timedelta(hours=2):
		return False

	return True


# check if meeting falls within the schedule
def check_schedule_conflict(date, start_time, end_time):
	date_format = '%Y-%m-%d'
	meeting_date = datetime.strptime(date, date_format)

	day = meeting_date.weekday()
	schedule = Schedule.objects.filter(day=day).first()

	# if user is busy the whole day
	if schedule.busy_day:
		return True

	time_format = '%H:%M:%S'
	# if meeting doesn't falls within the user schedule 
	if schedule.start_time <= datetime.strptime(start_time, time_format).time() and schedule.end_time >= datetime.strptime(end_time, time_format).time():
		return False

	# meeting is conflicting with he schedule
	return True


# checks if the meeting request overlaps with existing meetings 
def check_meeting_conflict(date, start_time, end_time):
	return Meeting.objects.filter(date=date, start_time__lt=end_time, end_time__gt=start_time).exists()

# creates meeting object
def add_meeting(date, client_email, start_time, end_time, busy=False):
	client = Client.objects.filter(email=client_email).first()
	Meeting.objects.create(user_id=1, client=client, date=date, start_time=start_time, end_time=end_time, busy=busy)

#######################################################


#generates dialogFlow response
def generate_response(messsage):
	response = {}
	response['speech'] = messsage
	response['displayText'] = messsage
	response['data'] = {}
	response['contextOut'] = []
	response['source'] = 'User'

	return response


def message_generator(res_type):
	meeting = (
		'Thank you for the invitation to meet with you on {} at {}. I am writing to accept your invitation and look forward to meeting with you and I look forward to a productive meeting with you.', 
		'I would like to take this opportunity to thank you for the meeting invite on {} at {}. I am writing to accept your invitation and look forward to a productive meeting.',
		'This is in reference to your meeting request. I am pleased to accept and will be meeting you on {} at {}.I would like to thank you for extending this offer to me and I commit I shall make the most of this meeting and give you no opportunity to disappoint you.'
	)

	no_meeting = (
		'I am afraid that I won\'t be available to meet you at the requested time due to prior engagements.',
		'I would be delighted to meet with you to discuss the business opportunities. However, I won\'t be available during this period so it would be great if we could reschedule our meeting to some other day.',
		'I regret to inform you that due to prior commitments I would be unable to make it to the proposed meeting.'
	)

	meeting_conflict = (
		'You already have another meeting scheduled at this time.',
		'Sorry! You already have other meetings lined up at the scheduled time.'
	)

	meeting_confirm = (
		'The meeting has been confirmed!',
		'Cheers! The meeting has been arranged.',
		'Your wish is my command. Meeting booked!'
	)

	lapsed = (
		'I regret that I cannot attend the requested meeting as the stated time period has elapsed.',
		'Thank you for the invitation. However I am afraid that we cannot proceed with this meeting as the stated time period has lapsed.'
	)

	open_salutation = (
		'Hi',
		'Dear Sir/Madam'
	)

	close_salutation = (
		'Regards',
		'Sincerely',
		'Faithfully'
	)

	cancel = (
		'{} meetings have been canceled!',
	)

	invalid = (
		'Sorry, can\'t do!',
		'I did not recognize that',
		'Pardon me!',
		'Invalid request'
	)

	name_not_found = (
		'I did not recognize that name. Add client!',
		'Client not found. Add client!'
	)

	return {
		'meeting': random.choice(meeting),
		'no-meeting': random.choice(no_meeting),
		'meeting-conflict': random.choice(meeting_conflict),
		'meeting-confirm': random.choice(meeting_confirm),
		'lapsed' : random.choice(lapsed),
		'open-salutation': random.choice(open_salutation),
		'close-salutation': random.choice(close_salutation),
		'cancel' : cancel[0],
		'invalid': random.choice(invalid),
		'name-not-found': random.choice(name_not_found)
	}[res_type]



############ CANCEL MEETINGS #############

# cancel all meetings on a given day
def cancel_by_date(data):
	parameter = data['result']['parameters']
	date = parameter['date']
	num = Meeting.objects.filter(date=date).delete()[0]

	if parameter['busy']:
		Meeting.objects.create(user_id=1, date=date, start_time='00:00:00', end_time='23:59:59', busy=True)


	return cancel_message(num)


# cancel meeting on a given time
def cancel_by_time(data):
	parameter = data['result']['parameters']
	time = parameter['time']
	date = parameter['date']

	num = Meeting.objects.filter(start_time=time, date=date).delete()[0]

	if parameter['busy']:
		Meeting.objects.create(user_id=1, date=date, start_time=time, end_time=calc_end_time(time), busy=True)

	return cancel_message(num)


# cancel meeting in a range
def cancel_by_range(data):
	parameter = data['result']['parameters']
	date = parameter['date']

	time_period = parameter['time-period']
	temp = time_period.split('/')

	start_time = temp[0]
	end_time = temp[1]

	num = Meeting.objects.filter(start_time__lt=end_time, end_time__gt=start_time, date=date).delete()[0]

	if parameter['busy']:
		Meeting.objects.create(user_id=1, date=date, start_time=start_time, end_time=end_time, busy=True)

	return cancel_message(num)


def cancel_message(num):
	message = message_generator('cancel').format(num)
	response = generate_response(message)
	return JsonResponse(response)


def schedule_client_meeting(data):

	parameter = data['result']['parameters']
	date = parameter['date']
	start_time = parameter['time']
	end_time = calc_end_time(start_time)
	name = parameter['name']
	email = parameter['email']

	message = ''

	if check_meeting_conflict(date, start_time, end_time):
		message = message_generator('meeting-conflict')

	elif name:
		client = Client.objects.filter(name__icontains=name).first()
		if client:
			Meeting.objects.create(user_id=1,  client=client, date=date, start_time=start_time, end_time=end_time, busy=False)
			message = message_generator('meeting-confirm')

		else:
			message = message_generator('name-not-found')


	elif email:
		client = Client.objects.filter(email=email).first()
		if not client:
			client = Client.objects.create(name=email, email=email)

		Meeting.objects.create(user_id=1,  client=client, date=date, start_time=start_time, end_time=end_time, busy=False)
		message = message_generator('meeting-confirm')

	else:
		message = message_generator('invalid')

	response = generate_response(message)
	return JsonResponse(response)



def add_client(data):
	parameter = data['result']['parameters']
	name = parameter['name']
	email = parameter['email']

	Client.objects.create(name=name, email=email)
	message = 'Client has been added'
	
	response = generate_response(message)
	return JsonResponse(response)


def client_list(data):

	clients = json.loads(json.dumps(list(Client.objects.values('name', 'email'))))
	message = 'Your clients are-'
	for i in clients:
		message = '{} : {}\n'.format(i['name'], i['email'])

	response = generate_response(message)
	return JsonResponse(response)