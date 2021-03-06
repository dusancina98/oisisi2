from Ostalo import globalVar
from StrukturePodataka.Skup import Skup
import re
from StrukturePodataka.stack import *

class TreeNode: # cvor stabla koje cemo kreirati
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def isOperator(c): # proverava da li je operator && || ili !
        if (c == "&&" or c == "||" or c == "!"):
            return True
        else:
            return False

def printPostorder(root):

    if root:
        printPostorder(root.left)
        printPostorder(root.right)
        print(root.value),

def kreirajStablo(postfix):
        stek = Stack()
        postfix = postfix.split()

        for char in postfix:

            if not isOperator(char): #  ako nije operand kreiramo cvor i stavljamo na stek
                t = TreeNode(char)
                stek.push(t)
            else:  # ako je operator
                if(char=="!"): # ako je uzvicnik kreiramo nov cvor od "!" a za levo dete stavimo vrh steka
                    t = TreeNode(char)
                    t.left = stek.pop()
                else: # ako je neki drugi operator kreiramo cvor i kao levo i desno dete stavljamo 2 stavke sa vrha steka
                    t = TreeNode(char)
                    t.right =stek.pop()
                    t.left = stek.pop()

                stek.push(t) # sta stek stavljamo cvor

        t = stek.pop() # kada prodje kroz for u steku ce se nalaziti samo root

        return t

def evaluacijaStabla(root):

    if root is None:
        return None

    if root.left is None and root.right is None:
        bool, skup = globalVar.GLOBAL_TRIE.search(root.value)
        if bool == "True":
            return skup
        else:
            return Skup()

    levo_podstablo = evaluacijaStabla(root.left)

    desno_podstablo = evaluacijaStabla(root.right)

    if root.value == "&&":
        return levo_podstablo & desno_podstablo
    elif root.value == "||":
        return levo_podstablo | desno_podstablo
    elif root.value == "!":
        return levo_podstablo.komplement(globalVar.NADSKUP)

def infixToPostfixGenerator(kriterijum): # proveriti da li brojac dobro radi!!!
    priority = {} # recnik koji cuva prioritete
    priority["!"]= 4 # najveci prioritet
    priority["&&"] = 3
    priority["||"] = 2
    priority["("] = 1

    stek= Stack();
    result = []
    #print(kriterijum)
    #kriterijum= kriterijum.split()
    #print(kriterijum)
    brojac = 0 # ukoliko se obicna rec u kriterijumu javi vise od 1 puta znaci da imamo test1 test2 (nije navedeno || izmedju) i moramo uzeti u obrzir

    for rec in kriterijum:
        if rec== "(":
            stek.push(rec) # ako je leva zagrada ide na stek
            brojac=0
        elif rec==")":  # ako je desna zagrada uzimamo vrednost sa vrhu i sve dok ona nije "(" unosimo reci u result (svaka zatvorena mora imati svoju otvorenu)
            vrhSteka= stek.pop()
            while vrhSteka != "(":
                result.append(vrhSteka)
                vrhSteka= stek.pop()
            brojac = 0
        elif rec=="!" or rec=="&&" or rec=="||":
            while(not stek.isEmpty() and priority[stek.peek()] >= priority[rec]): # sve dok nije prazan stek i ako je prioritet u steku veci od prioriteta rec
                result.append(stek.pop()) # u result upisujemo operaciju koja ima veci prioritet
            stek.push(rec) # kada zavrsi while petlju stavlja operaciju na vrh steka
            brojac = 0
        else:
            result.append(rec) # u slucaju da naidje obicna rec(u ovom slucaju ce biti kriterijum po kojem se pretrazuje) odmah upisuje u result
            if brojac>=1:
                result.append("||")
            brojac+=1

    while not stek.isEmpty(): # sve dok nije prazan stavljamo u result sve iz steka
        result.append(stek.pop())

    return " ".join(result)

def parsirajNapredniUnos(kriterijum):
        kriterijumArray = []
        returnValAnd = [] # niz koji cuva splitovano prema && i ||
        returnVal = []

        kriterijum = kriterijum.strip()
        kriterijum = kriterijum.replace('\t', '')
        kriterijumArray1 = re.split(' ', kriterijum)

        for ch in kriterijumArray1:
            if not ch == '':
                kriterijumArray.append(ch)

        if not "" in kriterijumArray:
            for criteria in kriterijumArray: # idemo kroz listu
                if "||" in criteria and "||" != criteria: # ako se || nalazi u kriterijumu a nije celo kriterijum
                    podstring = criteria.split("||") # podeli po ||
                    if "" in podstring: # ako imamo "" u podstingu(desice se kod ||test i test||) umesto toga stavi ||
                        for c in podstring:
                            if c=="":
                                returnValAnd.append("||")
                            else:
                                returnValAnd.append(c)
                    else: # u suprotnom
                        for criteriaOR in podstring:  # prolazimo kroz podstring
                            if "&&" not in criteriaOR: #ako u uslovu nema && onda ubacujemo uslov i dodajemo || sve kod ne dodjemo do poslednjeg kriterijuma
                                returnValAnd.append(criteriaOR)
                                if criteriaOR != podstring[len(podstring) - 1]:
                                    returnValAnd.append("||")
                            else: # ako imamo && onda njega delimo i ponavaljamo isti postupak
                                podstring2 = criteriaOR.split("&&")
                                for criteriaAND in podstring2:
                                    returnValAnd.append(criteriaAND)
                                    if criteriaAND != podstring2[len(podstring2) - 1]:
                                        returnValAnd.append("&&")
                                    elif criteriaOR != podstring[len(podstring) - 1]:
                                        returnValAnd.append("||")
                elif "&&" in criteria and "&&" != criteria: # isti princip kao za ||
                    #print(criteria)
                    podstring = criteria.split("&&")
                    if "" in podstring:
                        for c in podstring:
                            if c=="":
                                returnValAnd.append("&&")
                            else:
                                returnValAnd.append(c)
                    else:
                        for criteriaOR in podstring:
                            if "||" not in criteriaOR:
                                returnValAnd.append(criteriaOR)
                                if criteriaOR != podstring[len(podstring) - 1]:
                                    returnValAnd.append("&&")
                            else:
                                podstring2 = criteriaOR.split("||")
                                for criteriaAND in podstring2:
                                    returnValAnd.append(criteriaAND)
                                    if criteriaAND != podstring2[len(podstring2) - 1]:
                                        returnValAnd.append("||")
                                    elif criteriaOR != podstring[len(podstring) - 1]:
                                        returnValAnd.append("&&")
                else: # ako nemamo ni || ni && samo dodajemo kriterijum i u returnvaland imamo parsiran string po || i &&
                    returnValAnd.append(criteria)
            #print(returnValAnd)
            for criteria in returnValAnd:
                if criteria[0] == "(" and criteria != "(": # ako naidjemo na ( a nije ceo kriterijum ( moramo parsirati po zagradi
                    i=0
                    for c in criteria: # idemo po karakterima
                        if(c=="("): # ako naidjemo na zagradu upisujemo zagradu,isto i za !
                            returnVal.append("(")
                        elif c=="!":
                            returnVal.append("!")
                        else: # u suprotnom upisujemo ostatak stringa i zavrsavamo for
                            returnVal.append(criteria[i:])
                            break
                        i=i+1
                    """if criteria[1] == "!":
                        returnVal.append("(")
                        returnVal.append("!")
                        returnVal.append(criteria[2:])
                    elif criteria[1] == "(":
                        returnVal.append("(")
                        returnVal.append("(")
                        returnVal.append(criteria[2:])
                    else:
                        returnVal.append("(")
                        returnVal.append(criteria[1:])"""
                elif criteria[0] == "!" and criteria != "!":
                    i = 0
                    for c in criteria:
                        if (c == "("):
                            returnVal.append("(")
                        elif c == "!":
                            returnVal.append("!")
                        else:
                            returnVal.append(criteria[i:])
                            break
                        i = i + 1
                    """if (criteria[1] == "("):
                        returnVal.append("!")
                        returnVal.append("(")
                        returnVal.append(criteria[2:])
                    elif (criteria[1] == "!"):
                        returnVal.append("!")
                        returnVal.append("!")
                        returnVal.append(criteria[2:])
                    else:
                        returnVal.append("!")
                        returnVal.append(criteria[1:])"""
                elif criteria[len(criteria) - 1] == ")" and criteria != ")":
                    p=0
                    for i in range(1,len(criteria)):
                        if(criteria[-i]==")"): # idemo od pozadi i brojimo zagrade
                            #print("TEST")
                            p+=1
                        else:
                            break
                    returnVal.append(criteria[0:len(criteria)-p]) # upisemo prvih len-p karaktera
                    for i in range(0,p): # narednih p karaktera su zagrade
                        returnVal.append(")")



                    """returnVal.append(criteria[0:len(criteria) - 1])
                    returnVal.append(")")"""
                else:
                    returnVal.append(criteria)
            #print(returnVal)
            return returnVal
        else:
            return kriterijumArray

                                                 #ZA DULETA ! AKO TI TREBA TEST## TEST PRIMER: ( (test &&java ) 	&&    ! test) || !(test||java)
"""postfix = infixToPostfixGenerator("( dictionary list || set ) && ! tree")
r = kreirajStablo(postfix)
printPostorder(r)"""
