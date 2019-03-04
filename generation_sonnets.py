# -*- coding: utf-8 -*-

import random
import pickle
import json
from collections import Counter

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

def paramdate(rimes, cle):
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
    for sousListe in rimes:
        choix_date=[data for data in sousListe if data['id_sonnet'] in dico_intervalle[cle]]
        if len(choix_date)>0:
            choix_final.append(choix_date)
    
    return choix_final

def filter_by_authors(rimes, authors):
    """
    Find and return the rimes written by the given authors in the given rimes 
    Args:
        rimes: a list of rimes, each rime is a list of verses, each verse is a dict (texte, id, id_sonnet)
        authors: a list of authors
    Returns:
        a list of list. Same structure as the arg rimes but filtered by authors
    """
    liste_choix = [id_sonnet for id_sonnet in meta if meta[id_sonnet]['auteur'] in authors]
    # liste_choix=list()
    # for sonnet in meta:
    #     for i in auteurs: 
    #         if meta[sonnet]['auteur']== i:
    #             liste_choix.append(sonnet)

    choix_rimes=list()
    choix_final=list()
    for rime in rimes:
        choix_rimes = [verse for verse in rime if verse['id_sonnet'] in liste_choix]
        if len(choix_rimes) > 0:
            choix_final.append(choix_rimes)   
    return choix_final

def generate(authors='None', date='None', schema=('ABAB','ABAB','CCD','EDE')):
    all_rimes = types_rimes
    if date:
        contrainte_date = paramdate(all_rimes, date)  
        all_rimes = contrainte_date
    if authors: 
        contrainte_auteur = filter_by_authors(all_rimes, authors)
        all_rimes = contrainte_auteur
    longueur = len(all_rimes)

    schema_rimes = dict()
    # ('ABAB','ABAB','CCD','EDE') -> Counter({'A': 4, 'B': 4, 'C': 2, 'D': 2, 'E': 2})
    # le décompte de chaque lettre permet un traitement générique des schémas
    schema_letters = Counter(''.join(schema))
    while True :
        try :
            choix_rimes = random.sample(range(longueur), len(schema_letters))
            for i, letter in enumerate(schema_letters):
                current_rime = all_rimes[choix_rimes[i]]
                indexes = random.sample(range(len(current_rime)), schema_letters[letter])
                schema_rimes[letter] = [current_rime[index] for index in indexes]
            break
        except :
            continue

    sonnet = list()
    for stanza in schema:
        generated_stanza = list()
        for letter in stanza:
            verse = schema_rimes[letter].pop()
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
    sonnet = generate(authors=['Charles Baudelaire','Paul Verlaine', 'Sully Prudhomme'], date='1851-1870', schema=('ABBA','ABBA','EFG','HIJ'))
    for st in sonnet:
        for verse in st:
            print(verse['text'], verse['meta'])
        print()

if __name__ == "__main__":
    main()
