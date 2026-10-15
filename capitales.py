import sys
from random import randint
entryLenght = len(sys.argv) 
if entryLenght == 1 :
    raise ValueError ("Ce script a pour but d'être utilisé dans le terminal, avec 1 à 3 paramètres additionnels. ")
if entryLenght > 4  :
    raise ValueError ("Pour l'instant, il n'est pas possible d'utiliser ce programme avec plus de 3 arguments. ")




def allNumbers (list : list[str], b : int |None =0) -> bool : #b for begining
    """D'une liste de textes, détermine si tous sont des numéros. """
    allD = True
    n = b
    while allD and n < len(list) :
        if not (list[n]).isnumeric() : allD = False
        n += 1
    return allD 

if not(allNumbers(sys.argv[1:2])) :
    raise ValueError ("Les arguments de 'nombre de questions' et 'mode de fonctionnement' ne peuvent être que des nombres.")

def traitement(file ) -> list [tuple]  :
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

def capitalAsk (infos : tuple) -> bool:
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

def countryAsk (infos : tuple) -> bool :
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

def randomAsking(number : int , informations : list, mode : int | None = 1) -> tuple [int ,list[tuple[int, bool]]] : 
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


def savingDataEncoding(informations : list[tuple]) :
    """Retranscrire Les noms, comme ils étaient au départ, car ils ne sont pas récupérés à nouveau, donc introuvables"""
    data = ""
    for nameType, country, capital in informations :
        data = data + country + "("+nameType+")," + capital + "\n"
    return data
def savingAt(Data : str, maxTries : int | None = 3, mode : str | None = "w") :
    """Demande pour un nom de fichier pour sauvegarder les données avec un nombre d'essais limité"""
    tries = 0
    passed = False
    while tries < maxTries and not passed : 
        #J'ai trop le seum, y'aura pas d'erreur en fait.
        #la fonction open crée un fichier s'il n'existe pas...
        answer = input("À quel fichier ?")
        tries += 1
        try :
            file = open(answer,mode)
            file.write(Data)
            passed = True
        except FileNotFoundError :
            print("Le fichier n'a pas été trouvé.")
        except :
            print("Quelquechose s'est mal passé lors de la sauvegarde.")
            file.close()
        else :
            print("Fichier sauvegardé. ")
    file.close()
def savingIn (data : str,fileName : str | None= "CapitalesSave.csv") :
    """Crée un nouveau fichier qui contient les données envoyées. <br> On rajoute <b>(n)</b> si le nom était déjà utilisé  """
    opened = False
    tries = 0
    name = fileName
    while not opened and tries < 5:
        tries += 1
        try :
            file = open(name,"x")
            opened = True
        except FileExistsError:
            name = fileName
            dname = name.split(".") #découpé pour séparer de l'extension
            name = dname[0] + "("+ tries + ")" +"." + dname[1]   
        except :
            print("La sauvegarde s'est mal passée. ")  
            break
    if not opened :
        return
    try :
        file.write(data)
    except : print("La sauvegarde des données s'est mal passée.")
    file.close()


def selecting(resultList : list ,informations : list, filter : int | None = 0) :
    """Récupère les résutats en fonction d'un filtre : <i><b>Sans filtre, uniquement gagnants, uniquement perdants</b></i>"""
    if filter < 0 or filter > 2 :
        print("Niveau de filtre non reconnu, repositionné à 0")
    lastingData = []
    if filter == 0 :
        for index,result in resultList :
            lastingData.append(informations[index])
    elif filter == 1 :
        for index,result in resultList :
            if result : lastingData.append(informations[index])
    else : 
        for index,result in resultList :
            if not result : lastingData.append(informations[index])
    return lastingData


def proposeSaving(results : tuple, informations : list) :
    """Une fonction simple qui permet de poser des questions pour la sauvegarde et sauvegarder"""
    answer = (input("Veux-tu sauvegader quelquechose ? Si oui,quelle partie des résultats ?\n 1 = Tout, 2 = réussites, 3 = échecs")).strip()
    if not answer.isnumeric() :
        print("Format de chiffres non reconnu. ce sera un non.")
        answer = "0"
    ans = int(answer)
    if ans < 1 or ans > 4 :
        print("non. ok.")
        return
    
    selection = selecting(results,informations,(ans-1))
    selection = savingDataEncoding(selection)

    answer = input("Créer (0) ou utiliser (1) un fichier pour la sauvegarde ? ").strip()
    if not answer.isnumeric() :
        print("Format de nombre non reconnu. Création d'un nouveau fichier. ")
        answer = "0"
    ans = int(answer)
    
    if ans < 0 or ans > 1 :
        print("Valeur non attendue :", end="")
        ans = 0
    if ans == 0 :#à revoir
        print("création d'un nouveau dossier. ",end="")
        answer = input("Quel sera son nom ? :").strip()
        ndot = answer.count(".")
        if ndot == 0 and answer != "" : 
            answer = answer +".txt"
            print("Aucune extension, donc nom du fichier modifié : ",answer)
        elif ndot != 1 : answer = None
        if answer =="" : answer = None
        savingIn(selection, answer)
    if ans == 1 :
        answer = input("Ajout(1) or Écrasement(2) ? ")
        if not answer.isnumeric():
            print("Chiffre non reconnu, redirigé vers :")
            answer = "2"
        ans = int(answer)
        if ans == 1 :
            mode = "a"
            print("Ajout de texte.")
        else : 
            mode = "x"
            print("Écrasement.")
        savingAt(selection)


def fileTaker(fileName :str) :
    try :
        capFile = open(fileName, "r", encoding= "utf-8")
    except :
        print("The extraction of",fileName,"went wrong. ")
        return None
    return capFile

infoFileName = "Capitales.csv"
capFile : str = None
if entryLenght == 4 : #si on précise une liste
    wantedFile = sys.argv[3]
    capFile = fileTaker(wantedFile)
if capFile == None : 
    print("Trying to get the countries informations in", infoFileName+".")
    capFile = fileTaker(infoFileName)
    if capFile == None :
        print("The default file :",infoFileName,"has not been extracted well. \n try checking the paths")
        sys.exit()


questionNumber = int(sys.argv[1])  # 

mode : int= None
if len(sys.argv) > 2 : 
    mode = int(sys.argv[2])

countriesInfos = traitement(capFile)
capFile.close()
results = randomAsking(questionNumber, countriesInfos, mode)
print("Tu as eu un résultat de",results[0],"points.")