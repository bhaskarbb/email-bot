# email-bot
BotMail (Front-end): https://github.com/GauravB159/BotMail

An email bot that automatically schedules meetings based on emails received and displays the same through an interactive dashboard

Note: Need to install and run the front-end code seperately. Details in the provided URL

### Description
A bot that is connected to your gmail account. It reads all the incoming emails and if the email is related to meetings, it will try to have an email conversation with the client to set up a meeting. 

The user's schedule is created and displayed through an iteractive dashboard. Any changes can be made to this schedule using the GUI. An editional chat bot has been created to fullfil the same purpose.

### System Architecture

![Architecture](achitecture.PNG)

### Prerequisites
Python 3

### Installation

git clone https://github.com/bhaskar337/email-bot.git

cd email-bot/email-bot

pip install -r requirements.text

### To Run

python manage.py runserver

### Built With

1. Django 
1. Django-rest-framework
1. DialogFlow
