# -*- coding: utf-8 -*-

import random
import pickle

types_rimes = pickle.load(open('types_rimes.pickle', 'rb'))
    
def generate():    
    longueur = len(types_rimes)

    while True :
        try :
            choix_rimes=random.sample(range(longueur), 5)
            liste_A=random.sample(range(len(types_rimes[choix_rimes[0]])), 4)
            liste_B=random.sample(range(len(types_rimes[choix_rimes[1]])), 4)
            liste_C=random.sample(range(len(types_rimes[choix_rimes[2]])), 2)
            liste_D=random.sample(range(len(types_rimes[choix_rimes[3]])), 2)
            liste_E=random.sample(range(len(types_rimes[choix_rimes[4]])), 2)
            break

        except :
            continue

    sonnet = [types_rimes[choix_rimes[0]][liste_A[0]],
    types_rimes[choix_rimes[1]][liste_B[0]],
    types_rimes[choix_rimes[1]][liste_B[1]],
    types_rimes[choix_rimes[0]][liste_A[1]],
    '',
    types_rimes[choix_rimes[0]][liste_A[2]],
    types_rimes[choix_rimes[1]][liste_B[2]],
    types_rimes[choix_rimes[1]][liste_B[3]],
    types_rimes[choix_rimes[0]][liste_A[3]],
    '',
    types_rimes[choix_rimes[2]][liste_C[0]],
    types_rimes[choix_rimes[2]][liste_C[1]],
    types_rimes[choix_rimes[3]][liste_D[0]],
    '',
    types_rimes[choix_rimes[4]][liste_E[0]],
    types_rimes[choix_rimes[3]][liste_D[1]],
    types_rimes[choix_rimes[4]][liste_E[1]]]

    
    return sonnet


def main():
    sonnet = generate()
    for l in sonnet:
        print(l)

if __name__ == "__main__":
    main()