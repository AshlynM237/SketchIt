import json
from pprint import pprint
def loadPrompts():
    with open('hints.json') as f:
        x = json.load(f)
    return x

def loadWords():
    data= loadHints()
    options=[]
    for hint in data['words']:
        options.append(hint['word'])
    return options

def loadHints(word):
    '''Return the hints for the given word from the hints.json'''
    data = loadHints()
    pass
