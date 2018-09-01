import datetime
import rfc3339
import re
from textblob import TextBlob

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

string = '2pm 5pm 11pm 11am 12am 12pm'
strArr = [int(s) for s in re.findall(r'\d+',string)]
times, _, _ = find_cd(TextBlob(string))
print(times)
print(re.findall(r'\d+',times[0]))

def pm2clock(cardStr):
	number = re.findall(r'\d+',cardStr)
	if cardStr[len(number)] == 'a' and number != '12':
		return cardStr[0]
	elif cardStr[len(number)] == 'a' and number == '12':
		return '0'
	elif cardStr[len(number)] == 'p':
		return str(int(cardStr[0]) + 12)

print(pm2clock('4pm'))
print(pm2clock('4am'))

