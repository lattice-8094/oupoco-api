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

def paramdate(cle):
    erreur=[]
    for sonnet in meta:
        date=meta[sonnet]['date']
        if date=='Non renseignée':
            erreur.append(sonnet)

    dico_date=dict()
    for sonnet in meta:
        if sonnet not in erreur:
            dico_date[sonnet]=meta.get(sonnet) 

    intervalle_1=list()
    intervalle_2=list()
    intervalle_3=list()
    intervalle_4=list()
    intervalle_5=list()
    intervalle_6=list()
    dico_intervalle=dict()
    for key in dico_date:
        if dico_date[key]['date'] > '1800' and dico_date[key]['date'] <= '1830':
            intervalle_1.append(key)
        if dico_date[key]['date'] > '1830' and dico_date[key]['date'] <= '1850':
            intervalle_2.append(key)
        if dico_date[key]['date'] > '1850' and dico_date[key]['date'] <= '1870':
            intervalle_3.append(key)
        if dico_date[key]['date'] > '1870' and dico_date[key]['date'] <= '1890':
            intervalle_4.append(key)
        if dico_date[key]['date'] > '1890' and dico_date[key]['date'] <= '1900':
            intervalle_5.append(key)
        if dico_date[key]['date'] > '1900' and dico_date[key]['date'] <= '1950':
            intervalle_6.append(key)


    dico_intervalle={
        '1800-1830':intervalle_1,
        '1831-1850':intervalle_2,
        '1851-1870':intervalle_3,
        '1871-1890':intervalle_4,
        '1891-1900':intervalle_5,
        '1901-1950':intervalle_6}

    choix_final=list()
    choix_date = list()
    for sousListe in types_rimes:
        choix_date=[data for data in sousListe if data['id_sonnet'] in dico_intervalle[cle]]
        if len(choix_date)>0:
            choix_final.append(choix_date)
    
    return choix_final

def generate(schema=('ABAB','ABAB','CCD','EDE')):
    contrainte_date=paramdate('1831-1850')    
    longueur = len(contrainte_date)
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