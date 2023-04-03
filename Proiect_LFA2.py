# lambda nfa to nfa
# 1. lambda closure
# 2. foreach qi -l> qj -a> qk
#   draw vertex from qi to qk with a
# you now have nfa
# 2. nfa to dfa

import copy

#citim automatul

class Automat:

    def __init__(self):

        self.stari = list()
        self.alfabet = list()
        self.matriceTranzitii = list()
        self.stareInit = ""
        self.stariFinale = list()
        self.cuvinte = list()
        self.NFA = False
        self.solutii = list()
        self.lambdaStari = list()
        self.passed = list()
        self.lambdaInchidere = list()
        

    def readAutomat(self, fisier):

        with open(fisier, "r", encoding="utf-8") as fisierautomat:
            self.stari = [x for x in fisierautomat.readline().split()]
            self.passed = [0 for x in range(len(self.stari))] 
            #print(self.stari[0]) #todo debug
            self.stari[0] = self.stari[0][1:] #debug ca am mizerie unicode la inceput de fisier
            #print(self.stari)

            #initializam matricea de tranzitii
            self.matriceTranzitii = [[list() for x in range(len(self.stari))] for i in range(len(self.stari))] 
            #print(matriceTranzitii)

            self.alfabet = [x for x in fisierautomat.readline().strip('\n')]
            #print(self.alfabet)
            self.aux = fisierautomat.readlines()
            for i in range(len(self.aux) - 2):
                l = [x for x in self.aux[i].strip('\n').split()]

                #verificam daca am facut o greseala de redactare
                if l[0] not in self.stari:
                    raise ValueError(f"Starea {l[0]} nu este definita!")
                if l[2] not in self.stari:
                    raise ValueError(f"Starea {l[2]} nu este definita!")
                if l[1] not in self.alfabet and l[1] != 'λ':
                    raise ValueError(f"Litera {l[1]} nu este definita!")

                if l[1] == 'λ' and l[0] not in self.lambdaStari:
                    self.lambdaStari.append(l[0])

                #print(stari.index(l[0]))
                #print(stari.index(l[2]))

                # verificam daca avem de-a face cu nfa sau dfa
                for linie in self.matriceTranzitii[self.stari.index(l[0])]:
                    for caseta in linie:
                        if l[1] in caseta:
                            self.NFA = True

                self.matriceTranzitii[self.stari.index(l[0])][self.stari.index(l[2])].append(l[1])

            self.stareInit = self.aux[-2].strip('\n')
            self.stariFinale = [x for x in self.aux[-1].split()]

    def lambdaClosure(self):

        for stare in self.stari:
            self.passed = [0 for x in range(len(self.stari))]
            self.lambdaInchidere.append(self.DFS(stare, stare))
            
        for i in range(len(self.lambdaInchidere)):
            for elem in self.lambdaInchidere[i]:
                if 'λ' not in self.matriceTranzitii[i][self.stari.index(elem)]:
                    self.matriceTranzitii[i][self.stari.index(elem)].append('λ')

        for i in range(len(self.stari)):
            self.lambdaInchidere[i].append(self.stari[i])
        #stariNoi = copy.deepcopy([self.lambdaInchidere[i].append(self.stari[i]) for i in range(len(self.stari))])
        print(self.lambdaInchidere)

    def DFS(self, nodStart, nodCurent):
        if self.passed[self.stari.index(nodCurent)]: return #evitam cicluri infinite
        self.passed[self.stari.index(nodStart)] = 1

        for i in range(len(self.matriceTranzitii[self.stari.index(nodCurent)])):
            if 'λ' in self.matriceTranzitii[self.stari.index(nodCurent)][i]:
                self.DFS(nodStart, self.stari[i])
                self.passed[i] = 1

        ans = list()
        for i in range(len(self.passed)):
            if self.passed[i] == 1 and i != self.stari.index(nodStart):
                ans.append(self.stari[i])
        #print(ans)
        return ans

    def toNFA(self):

        #for i in self.matriceTranzitii:
        #    for j in i:
        #        print(j, end=' ')
        #    print()
        #print()

        cMatrice = copy.deepcopy(self.matriceTranzitii)
        bIsOk = True

        for i in range(len(cMatrice)):
            for j in range(len(cMatrice[i])):
                if 'λ' in cMatrice[i][j]:
                    if i == j: 
                        self.matriceTranzitii[i][j].remove('λ')
                        continue
                    bIsOk = False
                    self.matriceTranzitii[i][j].remove('λ')
                    # q1 lb q2 l q3 -> 
                    for k in range(len(cMatrice[j])):
                        for l in cMatrice[k][i]:
                            # am adaugat conditia de is not lambda
                            if l not in self.matriceTranzitii[k][j] and l != 'λ':
                                self.matriceTranzitii[k][j].append(l)
                    for k in range(len(cMatrice[j])):
                        for l in cMatrice[j][k]:
                            if l not in self.matriceTranzitii[i][k] and l != 'λ':
                                self.matriceTranzitii[i][k].append(l)
                    
        if not bIsOk: self.toNFA()
        
        

        return

    def toDFA(self):
        
        # pornesc cu lambda inchiderea nodului in!!!!
        lStari = [list(self.lambdaInchidere[self.stari.index(self.stareInit)])]
        print(lStari)
        nMatrice = [[list() for x in range(len(self.alfabet))]] 
        print(nMatrice)
        
        stariNoi = [self.stareInit]
        for i in range(len(self.stari)):
            for k in self.alfabet:
                stareNoua = list()
                for j in range(len(self.matriceTranzitii[i])):
                    if k in self.matriceTranzitii[i][j]:
                        stareNoua.append(self.stari[j])
                #print(stareNoua)
                if(stareNoua not in stariNoi and len(stareNoua) > 1):
                    stariNoi.append(stareNoua)
                if(len(stareNoua) == 1):
                    if (stareNoua[0] not in stariNoi):
                        stariNoi.append(stareNoua[0])

        nMatriceTranzitii = [[list() for x in range(len(stariNoi))] for i in range(len(stariNoi))] 
        nStariFinale = list()

        #self.stari = copy.deepcopy(stariNoi)
        #for i in nMatriceTranzitii:
        #    for j in i:
        #        print(j, end=' ')
        #    print()
        #print(self.stari)
        for el in stariNoi:
            for ell in self.stariFinale:
                if ell in el and ell not in nStariFinale:
                    nStariFinale.append(el)
        self.stariFinale = copy.deepcopy(nStariFinale)

        

        for i in range(len(stariNoi)):
            for k in self.alfabet:
                if type(stariNoi[i]) == type("1"):
                    #print(self.stari[i])
                    stareNoua = list()
                    for j in range(len(self.stari)):
                        if k in self.matriceTranzitii[self.stari.index(stariNoi[i])][j]:
                            stareNoua.append(self.stari[j])
                    #print(stareNoua)
                    if len(stareNoua) == 1:
                        stareNoua = stareNoua[0]
                    if (stareNoua != list()):
                        nMatriceTranzitii[i][stariNoi.index(stareNoua)].append(k)
                else:
                    stareNoua = list()
                    for el in stariNoi[i]:
                        for j in range(len(self.matriceTranzitii[self.stari.index(el)])):
                            if k in self.matriceTranzitii[self.stari.index(el)][j] and self.stari[j] not in stareNoua:
                                stareNoua.append(self.stari[j])
                    if len(stareNoua) == 1:
                        stareNoua = stareNoua[0]
                    #print(stareNoua)
                    if (stareNoua != list()):
                        nMatriceTranzitii[i][stariNoi.index(stareNoua)].append(k)
        self.stari = copy.deepcopy(stariNoi)
        self.matriceTranzitii = copy.deepcopy(nMatriceTranzitii)

        return 

        
    #afisam datele dupa citire
    def printData(self):

        print(self.stari)
        print(self.alfabet)
        print(self.stareInit)
        print(self.stariFinale)
        #print(self.NFA)
        #print(self.lambdaInchidere)

        for i in self.matriceTranzitii:
            for j in i:
                print(j, end=' ')
            print()

        #print(self.lambdaInchidere)

            
if __name__ == "__main__":
    x = Automat()
    x.readAutomat("automat.txt")
    #x.printData()
    x.lambdaClosure()
    x.printData()
    x.toNFA()
    x.printData()
    x.toDFA()
    #x.printData()
    #print(x.passed)
    #x.printData()