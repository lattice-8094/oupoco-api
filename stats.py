import generation_sonnets
import re
from collections import Counter

# multiplier entre eux les éléments d'une liste 
def multLst(liste):
    r = 1
    for e in liste:
        r *= e
    return r

# multiplier entre elles les valeurs d'un dico 
def multDic(dico):
    r = 1
    for key, value in dico.items():
        r *= value
    return r

# nombre d'arrangemant en tenant compte de l'ordre
def arrang(n, k):
    """Nombre des arrangements de n objets pris k à k"""
    if k>n:
        return 0
    x = 1
    i = n-k+1
    while i <= n:
        x *= i
        i += 1
    return x

# associer un texte au chiffre obtenu
def messageGrdNb(int):
    if int > 1000000000000000000000 :
        nbre = re.findall(r'^(.+)..................$',str(int))
        mess1 = "-> "+str(int) + " sonnets possibles"+"\n-> c'est à dire des trilliards de sonnets\n-> soit plus de "+str(nbre[0])+" milliards de milliards"
        
    elif int > 1000000000000000000 :
        nbre = re.findall(r'^(.+)..................$',str(int))
        mess1 = "-> "+str(int) + " sonnets possibles"+"\n-> c'est à dire des milliards de milliards de sonnets\n-> soit plus de " + str(nbre[0])+" mille milliards de milliards"

    elif int > 1000000000000000 :
        nbre = re.findall(r'^(.+)...............$',str(int))
        mess1 = "-> "+str(int) + " sonnets possibles"+"\n-> c'est à dire des billiards de sonnets\n-> soit plus de "+str(nbre[0])+" millions de milliards"

    elif int > 1000000000000 :
        nbre = re.findall(r'^(.+).........$',str(int))
        mess1 = "-> "+str(int) + " sonnets possibles"+"\n-> c'est à dire des billions de sonnets\n-> soit plus de "+str(nbre[0])+" milliards"

    elif int > 1000000000 :
        nbre = re.findall(r'^(.+).........$',str(int))
        mess1 = "-> "+str(int) + " sonnets possibles"+"\n-> c'est à dire des milliards de sonnets\n-> soit plus de "+str(nbre[0])+" milliards"
        
    elif int > 1000000 :
        nbre = re.findall(r'^(.+)......$',str(int))
        mess1 = "-> "+str(int) + " sonnets possibles"+"\n-> c'est à dire des millions de sonnets\n-> soit plus de "+str(nbre[0])+" millions"
        
    elif int > 1000 :
        nbre = re.findall(r'^(.+)...$',str(int))
        mess1 = "-> "+str(int) + " sonnets possibles"+"\n-> c'est à dire des milliers de sonnets\n-> soit plus de "+str(nbre[0])+" milliers"
        
    else:
        mess1 = "-> "+str(int) + " sonnets possibles"+"\n-> c'est à dire moins de mille"
    
    return mess1

# EXEMPLES DE REQUETES - aide perso
#resultat, meta, schema =  generation_sonnets.get_rhymes_for_stats(authors=['Alfred de Musset','José-Maria de Heredia'],quality='2')
resultat, schema = generation_sonnets.get_rhymes_for_stats(authors=["François Coppée","Théodore de Banville"],quality='3')

#resultat, meta, schema = generation_sonnets.get_rhymes_for_stats(authors="Victor Hugo",quality='2')
#resultat = generation_sonnets.get_rhymes_for_stats(authors=['Théodore de Banville'])
#resultat, meta, schema = generation_sonnets.get_rhymes_for_stats(quality='5')

print(schema)

print("===== rimes placées (comme queneau papier) ===")

cptRimePlace=list()

for rimePlace in resultat:
	cptRimePlace.append(len(resultat[rimePlace]))

print (cptRimePlace)

nbSonnets=multLst(cptRimePlace)
print (messageGrdNb(nbSonnets))

print("===== rimes déplacées ===")

# creer la liste ordonnée des lettres du schema
lettrePlace = [x for elem in schema for x in elem]
#print(lettrePlace)

# nbr de fois où apparaît une lattre dans le schéma
schema_letters = Counter(''.join(schema))
#print(schema_letters)

# compter le nombre de vers pour scune lettre donnée / nbr de rimes 
compteParLettre=dict()
i=0
for lettre in lettrePlace:
	if lettre in compteParLettre:
		compteParLettre[lettre]= compteParLettre.get(lettre)+cptRimePlace[i]
	else :
		compteParLettre[lettre]=cptRimePlace[i]
	i+=1

print("nbr de rimes par lettre :")
print(compteParLettre)

arrangParLettre=dict()
# calcul arrangement sans remise par lettre : A de p parmi n
for lettre, nOcc in schema_letters.items():
	nElem=compteParLettre[lettre]
	arrangParLettre[lettre]=arrang(nElem,nOcc)

print("nbr d'arrangement possible par lettre :")
print(arrangParLettre)

nbSonnetsDeplaces=multDic(arrangParLettre)
print (messageGrdNb(nbSonnetsDeplaces))