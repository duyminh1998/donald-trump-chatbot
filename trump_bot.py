import spacy
import pandas as pd
import random

nlp = spacy.load('en')

df = pd.read_csv('data/qa_pair.csv', encoding = 'ISO-8859-1')

questions_nlp = []
for i in range(len(df)):
    questions_nlp.append(nlp(df.at[i, "Question"]))

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

flag = True

print("POTUS Donald Trump: My name is POTUS Donald Trump. I will answer your queries about America. If you want to exit, type Bye!")

while (flag == True):
    user_response = input()
    user_response=user_response.lower()
    if (user_response != 'bye'):
        if (user_response=='thanks' or user_response=='thank you'):
            flag = False
            print("POTUS Donald Trump: You are welcome..")
        else:
            if (greeting(user_response) != None):
                print("POTUS Donald Trump: " + greeting(user_response))
            else:
                q_doc = nlp(user_response)
                similarity = []
                for i in range(len(questions_nlp)):
                        a_doc = questions_nlp[i]
                        similarity.append(q_doc.similarity(a_doc))
                print(df.loc[similarity.index(max(similarity)), "Answer"])
    else:
        flag = False
        print("POTUS Donald Trump: Bye! take care..")
