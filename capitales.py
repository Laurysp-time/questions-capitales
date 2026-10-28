import sys
from random import randint
from os.path import lexists #C'est juste pour dire si le fichier n'existe pas.(sans causer exprès FileExistsError)
entryLenght = len(sys.argv) 
if entryLenght == 1 :
    print("Ce script a pour but d'être utilisé dans le terminal, avec des paramètres additionnels. ") #NOTE : même s'il  y a moyen de faire sans.
if entryLenght > 6  :
    raise ValueError ("Ce ne serait pas bon de le faire tourner avec plus de 10 arguments ")


#changement fait : on ne décode pas le tout au départ.
def getTwoLists(list : list[str]) -> tuple[list[int], list[str]] :
    """En prévision et prération de plus de modularité pour d'autres sytèmes à venir.
    ~ 
    Différentie et convertie les int des strings en deux listes distinctes"""
    intList = []
    stringList = []
    for string in list :
        if string.isnumeric() : intList.append(int(string))
        else : stringList.append(string)
    return (intList,stringList)
rules = ["/n:","/m:","/s:","/of:","/sf:","/:"]#nombre;mode;savemode;originFile;saveFile;specifications
def fill(list1 : list, list2 : list, rElement = None, appAtFull : bool | None = False) -> list :
    """Remplis d'un liste selon une autre, les espaces considérés comme vides.
    ~
    pour fusionner après avoir séparé.
    """
    full = False
    l = len(list1)
    for var in list2 :
        if full :
            list1.append(var)
            continue
        if rElement in list1 :
            list1[list1.index(rElement)] = var
        else : 
            full = True
            if not appAtFull : 
                raise ValueError ("Plus de valeurs ont été données que le programme n'en récupère. À :", type(var).__name__,"=",var)
            list1.append(var)
    return list1

def understand(list: list[str],guide : list[str],gap :str | None = None) :
    """Permet de repositionnner et classer les entrées, selon une liste depréfixes.
    ~
    à voir plus tard s'il on ne force pas de signer d'abord...  
    <br><i>ça aurait pu entièrment marché mais, à cause des valeurs non signées...c compliqué</i>"""
    indicatedList = []
    notIndicated = []
    for i in range(len(guide)) :
        indicatedList.append(gap) 
    hasIndic = False
    for text in list :
        hasIndic = False
        position = 0
        for indic in guide :
            if text.startswith(indic) :
                indicatedList[position] = text.removeprefix(indic)
                hasIndic = True
            position += 1
        if (not hasIndic) :
            notIndicated.append(text)
    return (indicatedList, notIndicated) #pour éviter que ce qui n'est pas indiqué soit effacé.


def refering(args : tuple, l : list) : #sert à rien ? il faut les None, je crois, pour les questions. On retire les questions ?
    """Permet d'affecter à un tuple d'arguments une liste et de garder la valeur d'un élément si son parallèle a une valeur choisie. <i>(sinon None)</i>
    ~
    si le nombre des arguments donnés dépasse le nombre d'objets dans liste, il ne renvoie pas d'erreur."""
    arguments = list(args)
    lenA = len(args)
    index = 0
    while index < lenA and index < len(l) :
        if not(l[index] is None) :
            arguments[index] = l[index]
        index += 1
    return tuple(arguments)
    
def toIntVerify(list : list[str]) -> list[int] :
    """A dû être faite juste pour vérifier les valeurs pointées."""
    intlist = []
    for t in list : #-1 va être une des valeurs indicateurs
        if  t is None :
            intlist.append(t)
            continue
        if t == "" :#techniqement de sert que pour 1 seule variable
            intlist.append(-1)
            continue
        if t.isnumeric() :
            intlist.append(int(t))
        else :
            raise ValueError ("Une valeur pointée pour être un nombre n'en serait pas un : '" + t+"'")
    return intlist

def listBool(entry : str, guide : tuple) :
    modificators = []
    index = 0
    errors = 0
    for i in range(len(guide)) :
        modificators.append(False)
    if entry is None : return modificators
    for s in entry :
        if s in guide :
            modificators[guide.index(s)] = True
        else : errors += 1
        index += 1
    if errors > 0 : print("Il y a eu",errors,"erreur(s) au niveau des spécifications : spécification inconnue.")
    return modificators 


entries,unsigned = understand(sys.argv[1:],rules)
unsignI,unsignS = getTwoLists(unsigned)

entryInts = fill(toIntVerify(entries[:3]),unsignI) 
entryStrings = fill(entries[3:], unsignS)
nIntEntry = len(entryInts) #ça fait beaucoup là non ? ça sert à rien ? si on fait to int verify

defaultFileName = "Capitales.csv"
defaultSaveName = "CapitalesSave.csv"
infoFileName : str = defaultFileName
saveFileName : str = None
spécifications_Str : str = None #Peut-on faire qu'il prenne tous les trucs qui suivent, avec et/ou sans espaces ?
infoFileName,saveFileName,spécifications_Str = refering((infoFileName,saveFileName,spécifications_Str),entryStrings)
#vérifie que si on a marqué sans valeur, on mette la valeur déjà mise

spécifications_bool : list [bool]= listBool(spécifications_Str,["r","e","S"])
saveMode : int = None
saveType : int = None
if spécifications_bool[2] :
    saveMode = 1
    saveType = 1
    if (saveFileName is None) : saveFileName = defaultSaveName

questionNumber : int = 3
mode : int= 1
questionNumber,mode,saveMode = refering((questionNumber,mode,saveMode),entryInts) 

def parse(text:str) -> tuple : 
    if text == "" : return None 
    info = (text).split(",") # il y a ["country (type)","capital"]
    #print(info)  
    determiner = None
    cap2 = None #NOTE : None prend moins de place...et après on n'a qu'à faire 'is None'
    cap1 = info[1].strip()
    info = info[0].split("(") #on prend "country (type)" en ["country","type)"]

    country = info[0]
    if len(info) > 1 :
        determiner = info[1].removesuffix(")")
    if "/" in cap1 :
        caps = cap1.split("/")
        cap1 = caps[0].strip()
        cap2 = caps[1].strip()
        if cap2 == "" :
            cap2 = None
    return (determiner,country,(cap1,cap2)) #HACK : écoute, je voulais faire une classe, mais...

def comparateCapital(answer : str,cap : tuple[str]) :
    answer = answer.strip().lower()
    win = (cap[0].lower() == answer)
    if (not win) and (not (cap[1] is None)) :
        win = (cap[1].lower() == answer )
    return win
def capitalAsk (infos : tuple) -> bool:
    nameType, country, capitale = infos #the only we to transcript a tuple
    print ("Quelle est la capitale ", end = "")

    if nameType == "le" : print("du ", end="") #I made for evry case possible, technically
    elif nameType == "les" :print("des ", end= "")
    elif  (nameType == "la") or (nameType == "l'") :  print("de "+ nameType, end=" ") 
    elif (nameType is None) : print("de", end=" ") 
    else : print(nameType, end = " ")
 
    answer = input(country + " ? : ")
    stamement = comparateCapital(answer,capitale)
    if stamement : print("Bonne réponse !")
    else : print("Mauvaise réponse !")

    print("La réponse était : '"+capitale[0]+"'",end=" ")
    if not (capitale[1] is None) : print("ou "+"'"+capitale[1]+"'", end="")
    print()

    return stamement

def countryAsk (infos : tuple) -> bool :
    nameType, country, capitale = infos
    print( "Quel est le pays dont la capitale est ",end="")
    if capitale[1] is None :
        print(capitale[0], end="")
    else : print("'"+capitale[0]+"'"+" ou "+"'"+capitale[1]+"'")#HACK : à revoir
    print(" ? :", end= "")
    answer = input()
    statement = True
    if answer.lower().strip() != country.lower().strip() : 
        statement = False
    if statement : print("Bonne réponse !")
    else : print("Mauvaise réponse !")
    print("La réponse était :",nameType ,country)
    return statement
 
def alternateAsking (infos, n) -> bool:
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
    askWays = (capitalAsk,countryAsk,alternateAsking,randomAltAsk)
    try : 
        ask = askWays [mode - 1]
    except :  
        print("Mode de fonctionnement non reconnu, initialisé à 1. ") #à voir plus tard si jamais on veut redemander
        ask = (askWays[0])
    nU = len(informations)
    if nU < number :
        raise ArithmeticError ("Le nombre de questions est supérieur au nombre de pays disponibles")
    usableList = [i for i in range(nU)]
    usedList = []
    score = 0
    n = 0
    while n < number :
        radex = randint(0, nU - 1) #randomIndex
        index = usableList[radex]
        info = parse(informations[index])
        if not(info is None) :
            print()
            if mode != 3 : succeed = ask(info)
            else : succeed = ask(info,n)
            if succeed : score += 1
            usedList.append((index,succeed))
            n += 1

        usableList.pop(radex) #pour ne pas le retrouver
        nU -= 1
    return score, usedList

def resultPrint(usedList : list[int,bool],informations: list[tuple]) :
    for index, succeed in usedList :
        print("Pays :",informations[index][1], end="; ")
        print("Capitale :", informations[index][2], end= "; ")
        print("résultat :", end= " ")
        if succeed : print("-réussi-")
        else : print("-échoué-")


def savingAt(Data : str,Filename :str | None = "CapitalesSave.csv",mode : str | None = "w") -> bool :
    """sauvegarde un ficher à un emplacement, mode écrasement et mode ajout."""
    if not lexists(Filename) :
        print("le fichier n'existait pas, mais a été créé.")
    try :
        file = open(Filename,mode)
        file.write(Data)
    except :
        print("Quelquechose s'est mal passé lors de la sauvegarde.")
        file.close()
        return False
    else :
        print("Fichier sauvegardé. ")
    file.close()
    return True
def savingIn (data : str,fileName : str | None= "CapitalesSave.csv", maxTries : int | None = 5) -> bool :
    """Crée un nouveau fichier qui contient les données envoyées. <br> On rajoute <b>(n)</b> si le nom était déjà utilisé  """
    opened = False
    tries = 0
    name :str = fileName
    while not opened and tries < maxTries:
        tries += 1
        try :
            file = open(name,"x")
            opened = True
        except FileExistsError:
            dname = fileName.split(".") # séparer de l'extension
            name = dname[0] + "("+ str(tries) + ")" +"." + dname[1]   
        except Exception as e:
            print("La sauvegarde s'est mal passée. Erreur :"+type(e).__name__)  
            break
        else :
            print("le fichier " + name + " a été créé.")
    if not opened :
        print("Le nombre maximal d'essais de ",maxTries," est dépassé. Abandon de la sauvegarde.")
        return False
    try :
        #print(data)
        file.write(data)
        file.close()
    except Exception as e :
        print("La sauvegarde des données s'est mal passée.")
        print(type(e).__name__)
        return False
    else : return True
 
    
def selecting(resultList : list ,informations : list, filter : int | None = 0) :
    """Récupère les résutats en fonction d'un filtre : <i><b>Sans filtre, uniquement gagnants, uniquement perdants</b></i>
    <p> Rend un type <b><i>String</i></b>"""
    data = ""
    if filter == 1 :
        for index,result in resultList :
            if result : data += (informations[index]) + "\n"
    elif filter == 2 : 
        for index,result in resultList :
            if not result : data += (informations[index]) + "\n"
    else :
        if filter != 0 : print("Niveau de filtre non reconnu, repositionné à 0")
        for index,result in resultList :
            data += (informations[index]) + "\n"
        
    return data


def proposeSaving(results : tuple, informations : list[tuple],saveType : int, saveMode : int, saveFileName : str, defaultSaveName = "CapitalesSave.csv") :
    """Une fonction simple qui permet de poser des questions pour la sauvegarde et sauvegarder"""
    if saveType is None :
        answer = (input("Veux-tu sauvegader la session ? Si oui,quelle partie des résultats ?\n 1 = Tout, 2 = réussites, 3 = échecs ? ")).strip()
        if not answer.isdigit() :
            print("Format de chiffres non reconnu. ce sera un non.")
            return
        saveType = int(answer)
    if saveType < 1 or saveType > 4 :
        print("Nombre non attendu. Sauvegarde refusée.")
        return
    
    selection = selecting(results[1],informations,(saveType-1))#HACK : [1] car [0] est le nombre de bons...
    selectedData = selection#savingDataEncoding(selection)
    if saveMode is None :
        answer = input("Créer (1) ou utiliser (écrasement : 2, ajout :3) un fichier pour la sauvegarde ? ").strip()
        if answer.isdigit() :
            saveMode = int(answer)
        else :
            print("Format de nombre non reconnu. Création d'un nouveau fichier. ")
            saveMode = 1

    if saveMode < 1 or saveMode > 3 :
            print("Valeur de mode de sauvegarde non attendue :", end="")
            saveMode = 1

    if saveFileName is None :
        saveFileName = input("Quel sera son nom ? :").strip()
    if len(saveFileName) < 4  :
        saveFileName = defaultSaveName
        if saveFileName != "" :
            print("Nom de fichier trop court. Changé au nom par défaut : "+ saveFileName)
        
    if saveMode == 1 :
        print("création d'un nouveau fichier.")
        savingIn(selectedData, saveFileName)
          
    if saveMode > 1 :
        if saveMode == 2 :
            mode = "a"
            print("Ajout de texte.")
        else : 
            mode = "w"
            print("Écrasement.")
        savingAt(selectedData,saveFileName,mode)

def fileTaker(fileName :str) :
    """respect the <b>D.R.Y.</b> rule"""
    capFile = None
    try :
        capFile = open(fileName, "r", encoding= "utf-8")
    except FileNotFoundError :
        print("Le fichier du nom de '"+fileName+"' n'a pas été trouvé.")
    except Exception as er:
        print("la récupération du fichier",fileName," s'est mal passé. Erreur :", type(er).__name__)
        return None
    return capFile



if infoFileName != defaultFileName : 
    print("Récupère les information à partir du fichier : "+ infoFileName+".")
capFile = fileTaker(infoFileName)
if capFile is None :
    sys.exit()


countriesInfos = (capFile.read().split("\n"))
capFile.close()
results = randomAsking(questionNumber, countriesInfos, mode)
print("Tu as eu un résultat de",results[0],"points.")
if spécifications_bool[0] : 
    print()
    resultPrint(results[1],countriesInfos)
    print()
if not spécifications_bool[1] : proposeSaving(results,countriesInfos,saveType,saveMode,saveFileName) 

