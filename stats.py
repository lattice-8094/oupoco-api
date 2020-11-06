import generation_sonnets
import pandas
from itertools import chain 
from collections import Counter
import re
from collections import OrderedDict, defaultdict
import numpy as np

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

def compare(s, t):
	return sorted(s) == sorted(t)

def noIntersection_2_listes(L1, L2):
    """List[Int] * List[Int] -> List[Int]
    Retourne la non intersection des deux listes L1 et L2,
    avec L1 liste la plus complète (liste de référence)"""
    result = []
 
    for n in L1:
        if n not in L2 and n not in result:
            result.append(n)
    result.sort()
 
    return result

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

# NB : besoin d'avoir les variables vide ci-après
# -> permet de verifier dans le progr si elle existe
# comment faire si appel en argument de fonction pour vérif existence ?

#authors=''
# à matcher avec themes par exemple :
#authors=['François Coppée','Théodore de Banville'] 
# TODO : pb - parfois pas de Hugo (si les 3 demandés) / parfois pas l'1 des 2 (si que Coppée et Banville)
authors=['François Coppée','Théodore de Banville','Victor Hugo']
#authors=['Alfred de Musset']

#themes=''
themes=['Amour','Nature']

dates=''
#dates='1831-1850'

resultat, schema, metaUtil, meta = generation_sonnets.get_rhymes_for_stats(authors=authors,themes=themes,dates=dates,quality='3')

# rappel de ce que contient meta :
# print(meta)

print("===== rapartition globale des critères / nombre de sonnets ===")
# print(metaUtil)
if authors or themes or dates:
	varSelec = list()
	if authors:
		varSelec.append("auteur")
	if themes:
		varSelec.append("thème")
	if dates:
		varSelec.append("date")
	#print(metaUtil.groupby(['auteur','date','thème'])['index'].count())
	print(metaUtil.groupby(varSelec)['index'].count())
#print(metaUtil.groupby(['auteur','thème','index'])['index'].count())
#print(resultat)

# 2 méthodes de visualisation des metaUtil : GLOB (tout en 1 dico) / PAR_TYPE (1df par type de metaUtil)
# GLOB l'ensemble des metaUtil données
cptRimePlace=list()
cptMetaPlace=dict()

# PAR_TYPE df par type de meta
listeAuteurSonnet=[]
listeThemeSonnet=[]
listeDateSonnet=[]

for rimePlace, listeRime in resultat.items():
	# GLOB : créer un dico des métadonnes
	listParPlace=[]

	# PAR_TYPE
	lstAuteur=list()
	lstTheme=list()
	
	for dic in listeRime:

		for line in metaUtil.itertuples():
			if line.index == dic['id_sonnet']:
				# GLOB
				dicMeta={}
				if authors :
					dicMeta['auteur']=line.auteur
					# PAR_TYPE
					lstAuteur.append(line.auteur)
				if themes:
					dicMeta['thème']=line.thème
					# PAR_TYPE
					lstTheme.append(line.thème)

				listParPlace.append(dicMeta)

	# PAR_TYPE
	# calculer le nombre d'occ d'1 auteur par liste 
	# en sortie : une liste de dico (place dans la liste = num du vers)
	if authors :
		histAuteur = {}
		for e in lstAuteur:
		    histAuteur[e] = histAuteur.get(e, 0) + 1
		# sortie : [ {auteur:nbOcc,auteur2:nbOcc}, {....}, ...] => 14 dico dans la liste
		listeAuteurSonnet.append(histAuteur)

	if themes:
		histTheme = {}
		for t in lstTheme:
		    histTheme[t] = histTheme.get(t, 0) + 1
		# sortie : [ {auteur:nbOcc,auteur2:nbOcc}, {....}, ...] => 14 dico dans la liste
		listeThemeSonnet.append(histTheme)

	cptMetaPlace[rimePlace] = listParPlace

	cptRimePlace.append(len(resultat[rimePlace]))

print("#### meta ###")

# TODO alléger -> ? faire une fonction pour mutualiser le traitement des 3 critères 

if authors and len(authors)>1:
	print("## AUTEURS ##\ndataframe : ")

	dfAuteur = pandas.DataFrame(listeAuteurSonnet)
	# transposer le df (inverser col et ligne)
	dfAuteur_T=dfAuteur.T
	print(dfAuteur_T)

	print(" Respect du critère dans les comptes : ")

	# !!! la sélection aléatoire initiale ne reprend pas l'ensemble des auteurs demandés
	messageAuteur=""
	if compare(authors,list(dfAuteur_T.index.values)) == False:
		messageAuteur= "!!! Ensemble de sonnets sans " + str(", ".join(noIntersection_2_listes(authors,list(dfAuteur_T.index.values))))

	else :
		critereAuthors = authors
		# nombre de fois où il n'y pas NaN dans une colonne :
		# dfAuteur_T.notnull().sum()
		# si tout est Nan sauf 1 <=> alors le critère est forcément actif
		for index, nb_noNull in dfAuteur_T.notnull().sum().items():
			if nb_noNull == 1:
				# i = auteur (index du df) // value = nb d'occ 1.0, 2.0, ... ou Nan
				for i, value in dfAuteur_T[index].items():
					if np.isfinite(value) == True:
						if i in critereAuthors :
							del critereAuthors[critereAuthors.index(i)]

		if not(critereAuthors):
			messageAuteur = "Dans chacun des sonnets possibles, au moins un vers de chacun des auteurs."
		else:
			messageAuteur = "Dans chacun des sonnets possibles, certains sonnets sans vers de : " + str(", ".join(critereAuthors))
			# TODO calculer le nb de sonnets en moins

	print(messageAuteur)

#str(n for n in range(0,len(critereAuthors)))

print("## THEME ##\ndataframe : ")

if themes and len(themes)>1:
	
	dfTheme = pandas.DataFrame(listeThemeSonnet)
	# transposer le df (inverser col et ligne)
	dfTheme_T=dfTheme.T
	print(dfTheme_T)

	print(" Respect du critère dans les comptes : ")
	messageTheme=""
	if compare(themes,list(dfTheme_T.index.values)) == False:
		messageTheme= "!!! Ensemble de sonnets sans " + str(", ".join(noIntersection_2_listes(themes,list(dfTheme_T.index.values))))

	else:
		critereThemes = themes
		for index, nb_noNull in dfTheme_T.notnull().sum().items():
			if nb_noNull == 1:
				for i, value in dfTheme_T[index].items():
					if np.isfinite(value) == True:
						if i in critereThemes :
							del critereThemes[critereThemes.index(i)]

		if not(critereThemes):
			messageTheme="Dans chacun des sonnets possibles, au moins un vers de chacun des thèmes."
		else:
			messageTheme="Dans chacun des sonnets possibles, certains sonnets sans vers du thème : " + str(", ".join(critereThemes))
			# TODO calculer le nb de sonnets en moins

	print(messageTheme)

print("===== schema ===")
print(schema)

print("===== rimes placées (comme queneau papier) ===")
print (cptRimePlace)

nbSonnets=multLst(cptRimePlace)
print (messageGrdNb(nbSonnets))

#### CAS QUI NE NOUS INTERESSE PAS POUR L INSTANT
# # quand nécessaire -> décommenter tout ce qui suit
# print("===== rimes déplacées ===")

# # creer la liste ordonnée des lettres du schema
# lettrePlace = [x for elem in schema for x in elem]
# #print(lettrePlace)

# # nbr de fois où apparaît une lattre dans le schéma
# schema_letters = Counter(''.join(schema))
# #print(schema_letters)

# # compter le nombre de vers pour scune lettre donnée / nbr de rimes 
# compteParLettre=dict()
# i=0
# for lettre in lettrePlace:
# 	if lettre in compteParLettre:
# 		compteParLettre[lettre]= compteParLettre.get(lettre)+cptRimePlace[i]
# 	else :
# 		compteParLettre[lettre]=cptRimePlace[i]
# 	i+=1

# print("nbr de rimes par lettre :")
# print(compteParLettre)

# arrangParLettre=dict()
# # calcul arrangement sans remise par lettre : A de p parmi n
# for lettre, nOcc in schema_letters.items():
# 	nElem=compteParLettre[lettre]
# 	arrangParLettre[lettre]=arrang(nElem,nOcc)

# print("nbr d'arrangement possible par lettre :")
# print(arrangParLettre)

# nbSonnetsDeplaces=multDic(arrangParLettre)
# print (messageGrdNb(nbSonnetsDeplaces))
