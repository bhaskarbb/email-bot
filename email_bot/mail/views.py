from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from user.models import Client

# Create your views here.
import requests
import json

MAIL_SERVER = ''

import apiai
ai = apiai.ApiAI("5024b204fe004def95ee70793929c0f0")



def message_to_bot(message, client):

    request = ai.text_request()
    request.query = message

    response = request.getresponse().read().decode('utf-8')
    return json.loads(response)



@csrf_exempt
def recieve_mail(request):
    
    mails = process_request(request)['mail']
    for mail in mails:
        user = mail['to']
        client_email = mail['fromEmail']
        client_name = mail['fromName']
        message = mail['message']

        message = '<{}>{}'.format(client_email, message) 
        response = message_to_bot(message, user)

        message = response['result']['fulfillment']['speech']
        subject = 'Regarding meeting'
        send_mail(subject, message, 'xbox2752@gmail.com', [client_email])

        # if client doesn't exists, we add new client
        if not Client.objects.filter(email=client_email).exists():
            Client.objects.create(name=client_name, email=client_email)

    return HttpResponse(message, status=200)


# converts request body to json
def process_request(request):
    data = request.body.decode('utf-8')
    return json.loads(data)




