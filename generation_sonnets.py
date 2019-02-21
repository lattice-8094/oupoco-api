# -*- coding: utf-8 -*-

import random
import pickle
import json

#types_rimes = pickle.load(open('types_rimes.pickle', 'rb'))
types_rimes = json.load(open('bd_rimes.json', 'r'))
meta = json.load(open('bd_meta.json', 'r'))

def __verse2meta__(verse):
    """
    @param: verse (dict {'texte':'', 'id':'', 'id_sonnet': ''})
    """
    res = dict()
    res['text'] = verse['texte']
    res['meta'] = meta[verse['id_sonnet']]
    return res

def generate(schema):    
    longueur = len(types_rimes)
    rimes = dict()

    while True :
        try :
            choix_rimes=random.sample(range(longueur), 5)
            indexes_A=random.sample(range(len(types_rimes[choix_rimes[0]])), 4)
            rimes['A'] = [types_rimes[choix_rimes[0]][index] for index in indexes_A]
            indexes_B=random.sample(range(len(types_rimes[choix_rimes[1]])), 4)
            rimes['B'] = [types_rimes[choix_rimes[1]][index] for index in indexes_B]
            indexes_C=random.sample(range(len(types_rimes[choix_rimes[2]])), 2)
            rimes['C'] = [types_rimes[choix_rimes[2]][index] for index in indexes_C]
            indexes_D=random.sample(range(len(types_rimes[choix_rimes[3]])), 2)
            rimes['D'] = [types_rimes[choix_rimes[3]][index] for index in indexes_D]
            indexes_E=random.sample(range(len(types_rimes[choix_rimes[4]])), 2)
            rimes['E'] = [types_rimes[choix_rimes[4]][index] for index in indexes_E]
            break

        except :
            continue

    sonnet = list()
    for stanza in schema:
        generated_stanza = list()
        for letter in stanza:
            verse = rimes[letter].pop()
            generated_stanza.append(__verse2meta__(verse))
        sonnet.append(generated_stanza)
   
    return sonnet


def main():
    schema=(('A', 'B', 'B', 'A'), ('A', 'B', 'B', 'A'), ('C', 'C', 'D'), ('E', 'D', 'E'))
    sonnet = generate(schema)
    for st in sonnet:
        for verse in st:
            print(verse['text'])
        print()

if __name__ == "__main__":
    main()