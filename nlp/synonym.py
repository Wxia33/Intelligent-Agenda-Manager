from nltk.corpus import wordnet
import re
import nltk
from textblob import TextBlob
import dateparser

def find_pronoun(sent):
    """Given a sentence, find a preferred pronoun to respond with. Returns None if no candidate
    pronoun is found in the input"""
    pronoun = None

    for word, part_of_speech in sent.pos_tags:
        # Disambiguate pronouns
        if part_of_speech == 'PRP' and word.lower() == 'you':
            pronoun = 'I'
        elif part_of_speech == 'PRP' and word == 'I':
            # If the user mentioned themselves, then they will definitely be the pronoun
            pronoun = 'You'
    return pronoun

def find_verb(sent):
    verb = []
    pos = []
    for word, part_of_speech in sent.pos_tags:
        if part_of_speech.startswith('VB'):  # This is a verb
            verb.append(word)
            pos.append(part_of_speech)
    return verb, pos


def find_noun(sent):
    noun = []
    pos = []
    for word, part_of_speech in sent.pos_tags:
        if part_of_speech.startswith('NN'):  # This is a noun
            noun.append(word)
            pos.append(part_of_speech)
    return noun, pos

def find_adjective(sent):
    adj = []
    pos = []
    for word, part_of_speech in sent.pos_tags:
        if part_of_speech.startswith('JJ'):  # This is an adjective
            adj.append(word)
            pos.append(part_of_speech)
    return adj, pos

sentence = "september 6th"
parsed = TextBlob(sentence)
print(parsed.pos_tags)
print(" ")

'''
event = wordnet.synset('event.n.01').lemmas()
print([str(lemma.name()) for lemma in event])


print('  ')

schedule = wordnet.synset('schedule.n.01').lemmas()
print([str(lemma.name()) for lemma in schedule])

sentence = "schedule an event"

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

print(findWholeWord('event')(sentence))
print(findWholeWord('dule')(sentence))

scheduleSnip = 'study session 1pm to 3pm'
print(find_noun(TextBlob(scheduleSnip)))
for noun in find_noun(TextBlob(scheduleSnip))[0]:
	print(noun)
'''
print(dateparser.parse("next thursday"))

ordinalString = "this is the 43rd time and 2nd 3rd"
'''
reg = re.compile(r'\d+')
for i in reg.finditer(ordinalString):
	findIterArr = reg.finditer(ordinalString)
	print(ordinalString[findIterArr.start():findIterArr.start() + 4])
	ordinalString = ordinalString.replace(ordinalString[findIterArr.start():findIterArr.start() + 4],"")



print(ordinalString)
regex = re.findall(r'\d+', ordinalString)
print(regex)
'''
month = ['january','february','march','april','may','june','july','august','september','november','december']
monthStr = "This is in january but also in april"

for i in month:
	print(i in monthStr)