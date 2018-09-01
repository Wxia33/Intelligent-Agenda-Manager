from flask import Flask, request
from textblob import TextBlob
import requests
import re
import apiai
import json
import dateparser

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import rfc3339

from dateutil.parser import parse

import dateUtilParser

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

app = Flask(__name__)

ACCESS_TOKEN = ''
CLIENT_ACCESS_TOKEN = ''

ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

messageArr = [0]

def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)

def pm2clock(cardStr):
    number = re.findall(r'\d+',cardStr)
    if cardStr[len(number)] == 'a' and number != '12':
        return cardStr[0]
    elif cardStr[len(number)] == 'a' and number == '12':
        return '0'
    elif cardStr[len(number)] == 'p':
        return str(int(cardStr[0]) + 12)

@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    #print(data['entry'][0]['messaging'][0])
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    parsed = TextBlob(message)
    
    requestAPI = ai.text_request()
    requestAPI.session_id = "newagent-a3968"
    requestAPI.query = message
    
    response = requestAPI.getresponse()
    jsonResponse = json.loads(response.read().decode('UTF-8'))
    replyApiAi = str(jsonResponse['result']['fulfillment']['speech'])
    
    if(messageArr[0] == 1):
        messageArr[0] = 0
        eventNoun, eventTime, eventDayofWeek, eventMonth, eventDayofMonth = eventAndTime(parsed)
        times,_,_ = find_cd(parsed)
        year = 2017
        month = 9
        dayStart = 17
        dayEnd = 17
        #hourStart = int(pm2clock(times[0]))
        #hourEnd = int(pm2clock(times[1]))
        minuteStart = 0
        minuteEnd = 0
        eventName = eventNoun
        rfcBegin, rfcEnd = dateUtilParser.eventBeginandEnd(message)
        #eventStart = rfc3339.rfc3339(datetime.datetime(year, month, dayStart, hourStart, minuteStart))
        #eventEnd = rfc3339.rfc3339(datetime.datetime(year, month, dayEnd, hourEnd, minuteEnd))
        make_event(eventNoun, rfcBegin, rfcEnd)
        reply(sender, "Event Created!")
    else:
        reply(sender, replyApiAi)

    if (findWholeWord('event')(replyApiAi) != None):
        messageArr[0] = 1
    return "ok"

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def find_noun(sent):
    noun = []
    pos = []
    month = ['january','february','march','april','may','june','july','august','september','october','november','december']
    monthDict = {'january':0,'february':1,'march':2,'april':3,'may':4,'june':5,'july':6,'august':7,'september':8,'october':9,'november':10,'december':11}
    monthArr = []
    dayofWeek = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    dayofWeekArr = []
    for word, part_of_speech in sent.pos_tags:
        if part_of_speech.startswith('NN') or part_of_speech.startswith('NNP'):  # This is a noun
            if word in dayofWeek:
                dayofWeekArr.append(word)
            elif word in month:
                print(word)
                monthArr.append(monthDict[word])
            else:
                noun.append(word)
                pos.append(part_of_speech)
    return noun, dayofWeekArr, monthArr, pos

def find_cd(sent):
    cd = []
    pos = []
    ordinal = []
    for word, part_of_speech in sent.pos_tags:
        if part_of_speech.startswith('CD'):
        	if 'st' in word or 'nd' in word or 'rd' in word or 'th' in word:
        		ordinal.append(word)
        	else:
        		cd.append(word)
        		pos.append(part_of_speech)
    return cd, ordinal, pos

def eventAndTime(parsed):
	#replySentNoun = "Name of Event: "
	replySentNoun = ""
    #replySentCD = "Time of Event: "
	replySentCD = ""
    replySentDayofWeek = "Day of Week: "
	replySentMonth = "Month: "
	replySentDaysofMonth = "Days of Month: "
	if find_noun(parsed)[1] != None:
		for dayofWeek in find_noun(parsed)[1]:
			replySentDayofWeek = replySentDayofWeek + dayofWeek + " "
	if find_noun(parsed)[2] != None:
		for month in find_noun(parsed)[2]:
			replySentMonth = replySentMonth + month + " "
	for noun in find_noun(parsed)[0]:
		replySentNoun = replySentNoun + noun + " "
	for cd in find_cd(parsed)[0]:
		replySentCD = replySentCD + cd + " "
	for dayMonth in find_cd(parsed)[1]:
		replySentDaysofMonth = replySentDaysofMonth + dayMonth + " "
	return replySentNoun, replySentCD, replySentDayofWeek, replySentMonth, replySentDaysofMonth

def dateFinder(sent):
	dateArr = []
	reg = re.compile(r'\d+')
	for m in reg.finditer(ordinalString):
		dateArr.append(ordinalString[m.start():m.start() + 4])
	return dateArr

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def make_event(name, startime, endtime):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    eventNEW = {
        'summary': name,
        'start': {
        'dateTime': startime,
        'timeZone': 'America/Los_Angeles',
    },
        'end': {
        'dateTime': endtime,
        'timeZone': 'America/Los_Angeles',
    },
    }
    event = service.events().insert(calendarId='primary', body=eventNEW).execute()
    print('Event created: %s' % (event.get('htmlLink')))

if __name__ == '__main__':
    app.run(debug=True)