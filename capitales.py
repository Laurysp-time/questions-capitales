import sys
from random import randint
if len(sys.argv) == 1 :
    raise ValueError ("Ce script a pour but d'être utilisé dans le terminal, avec 1 ou 2 paramètres additionnels. ")
if len (sys.argv) > 3  :
    raise ValueError ("Pour l'instant, il n'est pas possible d'utiliser ce programme avec plus de deux arguments. ")



def allDigit (list, b=0) -> bool : #b for begining
    """D'une liste de textes, détermine si tous sont des numéros. """
    allD = True
    n = b
    while allD and n < len(list) :
        if not list[n].isdigit() : allD = False
        n += 1
    return allD 

if not(allDigit(sys.argv[1:])) :
    raise ValueError ("Les arguments de ce scipt ne peuvent être que des nombres.")

def traitement(file) -> list [tuple]  :
    """Récupère d'un fichier ouvert le contenu à partir d'un traitement, récupérant determinant , nom et capitale""" 
    infos = []
    cap = ""
    country = ""
    typeC = ""
    for line in ((file.read()).split("\n")) :#split au lieu de readlines car sinon on a des \n à la fin..
        if line == "" : break 
        info = (line).split(",") # il y a ["country (type)","capital"]
        #print(info)
        cap = info[1].strip()
        info = info[0].split("(") #on prend "country (type)" en ["country","type)"]
        country = info[0]
        if len(info) > 1 :
            typeC = info[1].replace(")", "")
        else : typeC = ""
        infos.append((typeC,country,cap))
    return infos

def capitalAsk (infos) -> bool:
    nameType, country, capitale = infos #the only we to transcript a tuple
    print ("Quelle est la capitale ", end = "")
    if nameType == "le" : print("du ", end="") #I made for evry case possible, technically
    elif nameType == "les" :print("des ", end= "")
    elif nameType == "la" or nameType == "l'" :  print("de "+ nameType, end=" ") 
    else : print(nameType, end = " ")
    print(country, end= " ? : ")
    answer = input()
    stamement = True
    if answer.lower().strip() != capitale.lower().strip() : stamement = False
    if stamement : print("Bonne réponse !")
    else : print("Mauvaise réponse !")
    print("La réponse était :", capitale)
    return stamement

def countryAsk (infos) -> bool :
    nameType, country, capitale = infos
    print( "Quel est le pays dont la capitale est",capitale, end = " ? : ")
    answer = input()
    statement = True
    if answer.lower().strip() != country.lower().strip() : 
        statement = False
    if statement : print("Bonne réponse !")
    else : print("Mauvaise réponse !")
    print("La réponse était :",nameType ,country)
    return statement

def alternatAsking (infos, n) -> bool:
    if (n%2) == 0 : return countryAsk(infos)
    else : return capitalAsk(infos)
def randomAltAsk(infos) -> bool :
    n = randint(0,1)
    if n== 0 : return capitalAsk(infos)
    else : return countryAsk(infos)

def randomAsking(number, informations, mode = 1) -> tuple [int ,list[tuple[int, bool]]] : 
    """Pose un certain nombre de questions, à partir d'une liste. <i>Utilise randInt. </i>
    ~
    Récupère le nombre de questions, les informations sur les pays et, optionellement, le mode de questionnement. 
    Retourne un tuple avec le score et la site des questions passées(en tuple index-résultat)."""
    askWays = (capitalAsk,countryAsk)
    try : ask = askWays [mode - 1]
    except :  
        print("Mode de fonctionnement non reconnu, initialisé à 1. ") #à voir plus tard si jamais on veut redemander
        ask = (askWays[0])
    nU = len(informations)
    if nU < number :
        raise ArithmeticError ("Le nombre de questions est supérieur au nombre de pays disponibles")
    usableList = [i for i in range(nU)]
    usedList = []
    score = 0
    for n in range(number) :
        radex = randint(0, nU - 1) #randomIndex
        index = usableList[radex]
        succeed = ask(informations[index])
        if succeed : score += 1

        usedList.append((index,succeed))
        usableList.pop(radex) #pour ne pas le retrouver
        nU -= 1
    return score, usedList

def resultPrint(usedList,informations) :
    for index, succeed in usedList :
        print("Pays :",informations[index][1], end=" ")
        print("Capitale :", informations[index][2], end= " ")
        print("résultat :", end= " ")
        if succeed : print("-réussi-.")
        else : print("-échoué-.")

try :
    capFile = open("capPartiel.csv", "r", encoding= "utf-8")
except :
    raise Exception ("The extraction went wrong. \n")

questionNumber = int(sys.argv[1]) # 
if len(sys.argv) > 2 : 
    mode = int(sys.argv[2])
else : mode = 1
countriesInfos = traitement(capFile)
capFile.close()
results = randomAsking(questionNumber, countriesInfos, mode)
print("Tu as eu un résultat de",results[0],"points.")