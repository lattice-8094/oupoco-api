# -*- coding: utf-8 -*-

import random
import pickle
import json

types_rimes = json.load(open('bd_rimes.json', 'r'))
meta = json.load(open('bd_meta.json', 'r'))

def __verse2txtmeta__(verse):
    """
    Turn a verse (dict bd_rimes.json) into a txtmeta dict 
    with a call to bd_meta.json to retrieve the appropriate meta
    Args:
        verse: dict {'texte':'', 'id':'', 'id_sonnet': ''} from bd_rimes.json
    Returns:
        A Dict with 'txt' and 'meta' keys {'txt':'', meta:''}
        'meta' value is a Dict
        { "auteur": "", "date": "", "titre sonnet": "", "titre recueil": ""}
    """
    res = dict()
    res['text'] = verse['texte']
    res['meta'] = meta[verse['id_sonnet']]
    return res

def generate(schema=('ABAB','ABAB','CCD','EDE')):    
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
            generated_stanza.append(__verse2txtmeta__(verse))
        sonnet.append(generated_stanza)
   
    return sonnet


def main():
    schemas = {
    'sonnet_sicilien':('ABAB','ABAB','CDE','CDE'),
    'sonnet_petrarquien':('ABBA','ABBA','CDE','CDE'),
    'sonnet_marotique':('ABBA','ABBA','CCD','EED'),
    'sonnet_francais':('ABBA','ABBA','CCD','EDE'),
    'sonnet_queneau':('ABAB','ABAB','CCD','EDE')
    }
    sonnet = generate(schemas['sonnet_sicilien'])
    for st in sonnet:
        for verse in st:
            print(verse['text'])
        print()

if __name__ == "__main__":
    main()