from autocorrect import Speller
import string 
from chatterbot.conversation import Statement
import json

def fix_typos_in_statement(statement: Statement):
    txt = statement.text.split()
    fnal=[]
    for i in txt:
        if i in string.punctuation: # avoid processing symbols
            fnal.append(i) 
            continue
        correct = Speller(i)
        fnal.append(correct)
    return json.loads(statement.decode('utf-8'))