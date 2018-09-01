import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer

train_text = state_union.raw("2005-GWBush.txt")
sample_text = state_union.raw("2006-GWBush.txt")

custom_sent_tokenizer = PunktSentenceTokenizer(train_text)

tokenized = custom_sent_tokenizer.tokenize(sample_text)

def process_content():
    try:
        for i in tokenized[5:]:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            #namedEnt = nltk.ne_chunk(tagged, binary=True)
            #namedEnt.draw()
            print(tagged)
    except Exception as e:
        print(str(e))


#process_content()

timeTok = custom_sent_tokenizer.tokenize('I will go to study at three-thirty pm or 4:40am or 12:30 pm White House')
print(timeTok)
words = nltk.word_tokenize(timeTok[0])
tagged = nltk.pos_tag(words)
namedEnt = nltk.ne_chunk(tagged, binary=True)
namedEnt.draw()
print(namedEnt)