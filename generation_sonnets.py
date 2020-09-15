# -*- coding: utf-8 -*-

import random
import pickle
import json
import pandas
import sys
import loguru
import re
from collections import Counter, defaultdict

from loguru import logger
logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")
#logger.add(sys.stderr, format="{time} {level} {message}", level="DEBUG")

#types_rimes = json.load(open('bd_rimes.json', 'r'))
rhymes_1 = json.load(open('rhymes_1.json', 'r'))
rhymes_2 = json.load(open('rhymes_2.json', 'r'))
rhymes_3 = json.load(open('rhymes_3.json', 'r'))

meta = pandas.read_json(open('bd_meta.json'), orient='index')
schemas = {
    'sonnet_sicilien1':('ABAB','ABAB','CDE','CDE'),
    'sonnet_sicilien2':('ABAB','ABAB','CDC','CDC'),
    'sonnet_petrarquien1':('ABBA','ABBA','CDE','CDE'),
    'sonnet_petrarquien2':('ABBA','ABBA','CDC','DCD'),
    'sonnet_petrarquien3':('ABBA','ABBA','CDE','DCE'),
    'sonnet_marotique':('ABBA','ABBA','CCD','EED'),
    'sonnet_francais':('ABBA','ABBA','CCD','EDE'),
    'sonnet_queneau':('ABAB','ABAB','CCD','EDE'),
    'sonnet_shakespearien':('ABAB','CDCD','EFEF','GG'),
    'sonnet_spencerien':('ABAB','BCBC','CDCD','EE'),
    'sonnet_irrationnel':('AAB','C','BAAB','C','CDCCD')
    }
dates = ('1800-1830', '1831-1850', '1851-1870', '1871-1890', '1891-1900', '1901-1950')
sonnets_min_len = 3

def __get_last_word__(sentence):
    """
    Returns the last word of a sentence
    """
    words = sentence.split(' ')
    if re.search(r'[a-z]', words[-1]):
        last = words[-1]
    else:
        last = words[-2]
    last = re.sub(r"^.'",'', last, re.U)
    last = re.sub(r'\W','', last, re.U)
    return last

def __verse2txtmeta__(verse):
    """
    Turn a verse (dict bd_rimes.json) into a txtmeta dict 
    with a call to meta df to retrieve the appropriate meta
    Args:
        verse: dict {'texte':'', 'id':'', 'id_sonnet': ''} from bd_rimes.json
    Returns:
        A Dict with 'txt' and 'meta' keys {'txt':'', meta:''}
        'meta' value is a Dict
        { "auteur": "", "date": "", "titre sonnet": "", "titre recueil": ""}
    """
    res = dict()
    res['text'] = verse['text']
    res['meta'] = dict(meta.loc[verse['id_sonnet']])
    return res

def __compute_constraints__(constraints):
    """
    Args:
        - constraints: dict of field: list of values (list)
    """
    clause = ""
    if not(constraints):
        return ""
    else:
        for i, field in enumerate(constraints):
            if field == 'date':
                clause += '('
                if i != 0:
                    clause += "& "
                for j, interval in enumerate(constraints[field]):
                    start, end = [int(val) for val in interval.split('-')]
                    if j != 0:
                        clause += "or "
                    clause += f"({field} >= {start}) & ({field} <= {end}) "
                clause += ') '
            else: 
                # the constraint value is a list, we use 'isin'
                if i != 0:
                    clause += "& "
                clause += f"({field}.isin({constraints[field]})) "
    return clause

def __dates_to_intervals__(dates_list, intervals=dates):
    """
    Turn the given dates list into a set of intervals
    Args:
        - dates_list (list): list of dates
        - intervals (set): set of date intervals
    Returns:
        - set of date intervals
    """
    res = set()
    for date in dates_list:
        for begin, end in [interval.split('-') for interval in intervals]:
            if  int(date) >= int(begin) and date <= int(end):
                res.add(f"{begin}-{end}")
    return res

def get_dates(authors=[], themes=[]):
    """
    Query the db, returns the list of dates
    according to the given args
    Args:
        - authors: list of str
        - themes: list of str
    Returns:
        - list of dates intervals in the oupoco db
    """
    constraints = {}
    if themes:
        constraints['thème'] = themes
    if authors:
        constraints['auteur'] = authors
    my_query = __compute_constraints__(constraints)
    if my_query:
        df = meta.query(my_query)
        res = __dates_to_intervals__(set(df['date']))
    else:
        res = dates
    return res

def get_authors(dates=[], themes=[]):
    """
    Query the db, returns the list of authors
    according to the given args
    Args:
        - dates (list):  list of dates intervals (start-end)
        - themes (list): list of str
    Returns:
        - list of authors in the oupoco db
    """
    constraints = {}
    if dates:
        constraints['date'] = dates
    if themes:
        constraints['thème'] = themes
    my_query = __compute_constraints__(constraints)
    if my_query:
        df = meta.query(my_query)
        res = set(df['auteur'])
    else:
        res = set(meta.auteur)
    return res

def get_themes(dates=[], authors=[]):
    """
    Query the db, returns the list of themes
    according to the given args
    Args:
        - date (list): list of dates intervals (start-end)
        - authors (list): list of str
    Returns:
        - list of themes in the oupoco db
    """
    constraints = {}
    if dates:
        constraints['date'] = dates
    if authors:
        constraints['auteur'] = authors
    my_query = __compute_constraints__(constraints)

    if my_query:
        df = meta.query(my_query)
        res = set(df['thème'])
    else:
        res = set(meta.thème)
    return res

def filter_by_dates(dates_intervals, rhymes):
    """
    Find and return the rhymes published in the given dates in the given rhymes 
    Args:
        dates_intervals: a list of dates intervals
        rhymes: a list of ryhmes dict, each rhymes dict is itself a dict (rhyme: list of verses), each verse is a dict (text, id, id_sonnet)
    Returns:
        a list of dicts. Same structure as the rhymes but filtered by dates
    """
    sonnets = []
    for dates_interval in dates_intervals:
        start, end = dates_interval.split('-')
        df = meta.query(f"(date >= {int(start)}) & (date <= {int(end)})")
        sonnets.extend(df.index)
    #print(len(sonnets))
    if len(sonnets) < sonnets_min_len:
        return list()

    res = []
    # for each rhyme type (if rimes riches and suffisantes selected for instance)
    for rhymes_t in rhymes:
        rhymes_dates_d = {}
        for rhyme_sound, items in rhymes_t.items():
            verses = [verse for verse in items if verse['id_sonnet'] in sonnets]
            if len(verses) > 0:
                rhymes_dates_d[rhyme_sound] = verses
        res.append(rhymes_dates_d)
    return res

def filter_by_theme(themes, rhymes):
    """
    Find and return the rhymes categorized by the given theme or themes in the given rhymes 
    Args:
        themes: a list of themes
        rhymes: a list of ryhmes dict, each rhymes dict is itself a dict (rhyme: list of verses), each verse is a dict (text, id, id_sonnet)
    Returns:
        a list of dicts. Same structure as the rhymes but filtered by themes
    """
    sonnets = [id_sonnet for id_sonnet in meta.index if meta.loc[id_sonnet]['thème'] in themes]
    if len(sonnets) < sonnets_min_len:
        return list()

    res = []
    # for each rhyme type (if rimes riches and suffisantes selected for instance)
    for rhymes_t in rhymes:
        rhymes_themes_d = {}
        for rhyme_sound, items in rhymes_t.items():
            verses = [verse for verse in items if verse['id_sonnet'] in sonnets]
            if len(verses) > 0:
                rhymes_themes_d[rhyme_sound] = verses
        res.append(rhymes_themes_d)
    return res

def filter_by_authors(authors, rhymes):
    """
    Find and return the rhymes written by the given authors in the given rhymes 
    Args:
        authors: a list of authors
        rhymes: a list of ryhmes dict, each rhymes dict is itself a dict (rhyme: list of verses), each verse is a dict (text, id, id_sonnet)
    Returns:
        a list of dicts. Same structure as the rhymmes but filtered by authors
    """
    sonnets = [id_sonnet for id_sonnet in meta.index if meta.loc[id_sonnet]['auteur'] in authors]
    if len(sonnets) < sonnets_min_len:
        return list()

    res = []
    # for each rhyme type (if rimes riches and suffisantes selected for instance)
    for rhymes_t in rhymes:
        rhymes_authors_d = {}
        for rhyme_sound, items in rhymes_t.items():
            verses = [verse for verse in items if verse['id_sonnet'] in sonnets]
            if len(verses) > 0:
                rhymes_authors_d[rhyme_sound] = verses
        res.append(rhymes_authors_d)
    return res

def cpt_verse_position(id):
    """
    computes and returns the verse position thanks to the 'id' param
    Args:
        id: a string with the sonnet id, the stanza number (1 to 4), the verse position in stanza
    Returns:
        the verse position in sonnet (int)
    """
    (id_st, pos_st) = id.split("-")[-2:]
    pos_sonnet = int(pos_st)
    if id_st == "2":
        pos_sonnet += 4
    elif id_st == "3":
        pos_sonnet += 8
    elif id_st == "4":
        pos_sonnet += 11
    return pos_sonnet

def generate(order=True, authors='', dates='', schema=('ABAB','ABAB','CCD','EDE'), themes='', quality='1'):
    """
    Heart of the module, generate a new sonnet based on the desired constraints
    Args:
        order (boolean): wether the verses have to be placed in the same order as in the original sonnets
        authors (list): reduce the database to the desired authors
        dates (list): reduce the database to the desired dates intervals
        schema (tuple): the verses schema
        quality (str): quality of the rhyme. Except a value between 1 and 5.
                1: rimes pauvres, 2: rimes pauvres et suffisantes, 3: rimes suffisantes, 4: rimes suffisantes et rimes riches, 5: rimes riches
    Returns:
        the sonnet as a list of list (stanza ) of dict (verse)
    """
    rhymes_quality = {'1':[rhymes_1], '2':[rhymes_1, rhymes_2], '3':[rhymes_2], '4':[rhymes_2, rhymes_3], '5':[rhymes_3]}
    rhymes = rhymes_quality[quality]
    if dates:
        rhymes = filter_by_dates(dates, rhymes)
    if authors: 
        rhymes = filter_by_authors(authors, rhymes)
    if themes:
        rhymes = filter_by_theme(themes, rhymes)
    nb_rhymes = sum([len(rhyme_t.keys()) for rhyme_t in rhymes])

    random_rhymes = dict()
    # ('ABAB','ABAB','CCD','EDE') -> Counter({'A': 4, 'B': 4, 'C': 2, 'D': 2, 'E': 2})
    # le décompte de chaque lettre permet un traitement générique des schémas
    schema_letters = Counter(''.join(schema))
    # si moins de rimes dispos que de rimes nécessaires dans le schéma
    if nb_rhymes < len(schema_letters):
        logger.info("Nombre de rimes disponibles : {}, nombre de rimes nécessaires {}", nb_rhymes, len(schema_letters))
        return None

    # hack sale pour les rimes riches
    #if quality == '4' or quality == '5':
    #    order = False

    random_rhymes = generate_random_rhymes(schema, rhymes, order)
    sonnet = list()
    for stanza in schema:
        generated_stanza = list()
        for letter in stanza:
            verse = random_rhymes[letter].pop(0)
            generated_stanza.append(__verse2txtmeta__(verse))
        sonnet.append(generated_stanza)
   
    return sonnet

def generate_random_rhymes(schema, rhymes, order=True):
    """
    For each letter of the given schema, random choose a rhyme type and in the
    chosen rhyme type, random select the appropriate number of verses.
    Raise an OupocoException if the number of verses is inadequate.
    Args:
        schema (tuple): the verses schema
        rhymes (dict): a list of ryhmes dict, each rhymes dict is itself a dict (rhyme: list of verses), each verse is a dict (text, id, id_sonnet)
        order (boolean): wether the verses have to be placed in the same order as in the original sonnets
    Returns:
        a dict of list: the letters of the schema as keys, list of randomly picked verses as values
    """
    schema_letters = Counter(''.join(schema))
    schema_str = ''.join(schema)
    letter_rhymes_t = dict()

    # the type of rhymes for each letter of the schema
    # to be sure that each type is represented, we allocate one letter to each type
    for rhymes_t, random_letter in zip(rhymes, random.sample(list(schema_letters.keys()), len(rhymes))):
        letter_rhymes_t[random_letter] = rhymes_t
    # the remaining letters are randomly chosen
    for letter in schema_letters:
        if not(letter in letter_rhymes_t):
            letter_rhymes_t[letter] = random.choice(rhymes)
    
    while True:
        selected_rhymes = []
        schema_rhymes = defaultdict(list)
        try :
            letter_random_rhymes = {}
            letter_random_rhymes_2 = {}
            # Random pick a rhyme for each letter of the schema
            for letter in schema_letters:
                nb_verses = schema_letters[letter]
                rhymes_t = letter_rhymes_t[letter]
                random_rhyme = random.choice(list(rhymes_t.keys()))
                logger.debug("chosen rhyme for letter {} : {}", letter, random_rhyme)
                if random_rhyme in selected_rhymes:
                    raise Exception("All rhymes have to be different in a sonnet")
                else:
                    selected_rhymes.append(random_rhyme)
                    letter_random_rhymes[letter] = rhymes_t[random_rhyme]
                    letter_random_rhymes_2[letter] = random_rhyme # for debug only
            # Random pick a verse of the appropriate rhyme 
            for i, letter in enumerate(schema_str, 1):
                if order:
                    verses_in_position = [verse for verse in letter_random_rhymes[letter] if cpt_verse_position(verse['id']) == i]
                    logger.debug("{} vers de la rime {} en position {}", len(verses_in_position), letter_random_rhymes_2[letter], i)
                    current_verse = random.choice(verses_in_position)
                else:
                    current_verse = random.choice(letter_random_rhymes[letter])
                if __get_last_word__(current_verse['text']) in [__get_last_word__(verse['text']) for verse in schema_rhymes[letter]]:
                    raise Exception(f"Same word cannot be repeated in a rhyme {__get_last_word__(current_verse['text'])}")
                schema_rhymes[letter].append(current_verse)  
            break
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logger.info(message)
            continue

    return schema_rhymes

def generate_random_schema(graphic_difference=True):
    if graphic_difference:
        # seulement les schémas avec des rendus graphiques différents
        random_schema = random.choice(['sonnet_francais', 'sonnet_shakespearien', 'sonnet_irrationnel'])
    else:
        # tous les schémas
        random_schema = random.choice(list(schemas.keys()))
    sonnet = generate(order=True, schema=schemas[random_schema])
    rendered_sonnet = ""
    for st in sonnet:
        for verse in st:
            rendered_sonnet += verse['text']
            rendered_sonnet += "\n"
        rendered_sonnet += "\n"
    return(rendered_sonnet)

def main():
    sonnet = generate(order=False, schema=(schemas['sonnet_francais']), quality='5')
    if sonnet:
        for st in sonnet:
            for verse in st:
                print(verse)
                #print(verse['text'], verse['id'])
            print()
    else:
        print('Nope')

if __name__ == "__main__":
    main()
