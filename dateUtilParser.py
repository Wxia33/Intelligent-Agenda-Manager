import rfc3339
import datetime
import ner
from dateutil.parser import parse
from textblob import TextBlob

def eventBeginandEnd(sentence):
    times, dates, _ = ner.find_cd(TextBlob(sentence))
    beginTime = parse(times[0], fuzzy_with_tokens = True)[0] #Assume only 2 time frames
    endTime = parse(times[1], fuzzy_with_tokens = True)[0]

    dayOf = parse(dates[0], fuzzy_with_tokens = True)[0].day

    correctedBeginTime = datetime.datetime(2017, 9, dayOf, beginTime.hour, beginTime.minute)
    correctedEndTime = datetime.datetime(2017, 9, dayOf, endTime.hour, endTime.minute)
    rfcBegin = rfc3339.rfc3339(correctedBeginTime)
    rfcEnd = rfc3339.rfc3339(correctedEndTime)
    return rfcBegin, rfcEnd
'''
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
'''


