from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Test

# Create your views here.
@csrf_exempt
def action(request):

	if request.method == 'POST':

		request_data = str(request.POST)
		Test.objects.create(request=request_data)

		response = generate_response('Hello good isr')
		return JsonResponse(response)



def generate_response(messsage):
	response = {}
	response['speech'] = messsage
	response['displayText'] = messsage
	response['data'] = {}
	response['contextOut'] = []
	response['source'] = 'Hello'

	return response