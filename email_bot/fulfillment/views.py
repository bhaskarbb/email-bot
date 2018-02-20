from django.views.decorators.csrf import csrf_exempt

from meeting.views import schedule_meeting, cancel_by_time, cancel_by_date, cancel_by_range, schedule_client_meeting, add_client, client_list

import json


action_list = {
	'schedule-meeting' : schedule_meeting,
	'cancel-by-date' : cancel_by_date,
	'cancel-by-range': cancel_by_range,
	'cancel-by-time': cancel_by_time,
	'schedule-client-meeting': schedule_client_meeting,
	'add-client': add_client,
	'client-list': client_list
}	

# converts request body to json
def process_request(request):
	data = request.body.decode('utf-8')
	return json.loads(data)


@csrf_exempt
def action_handler(request):

	if request.method == 'POST':
		data = process_request(request)
		action = data['result']['action']
		return action_list[action](data)


