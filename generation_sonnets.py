# -*- coding: utf-8 -*-

import random
import pickle

types_rimes = pickle.load(open('types_rimes.pickle', 'rb'))
    
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
        for letter in stanza:
            sonnet.append(rimes[letter].pop())
        sonnet.append('')
   
    return sonnet


def main():
    schema=(('A', 'B', 'B', 'A'), ('A', 'B', 'B', 'A'), ('C', 'C', 'D'), ('E', 'D', 'E'))
    sonnet = generate(schema)
    for l in sonnet:
        print(l)

if __name__ == "__main__":
    main()