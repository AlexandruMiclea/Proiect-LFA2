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
            self.stari[0] = self.stari[0][-2:] #debug ca am mizerie unicode la inceput de fisier
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

    def toNFA():

          #todo implement
          #ideea e ca pentru fiecare nod unde am lambda apoi litera, sterg lambda si bag litera

        
    #afisam datele dupa citire
    def printData(self):

        print(self.stari)
        print(self.alfabet)
        print(self.stareInit)
        print(self.stariFinale)
        print(self.NFA)
        print(self.lambdaStari)

        for i in self.matriceTranzitii:
            for j in i:
                print(j, end=' ')
            print()

        print(self.lambdaInchidere)

            
if __name__ == "__main__":
    x = Automat()
    x.readAutomat("automat.txt")
    #x.printData()
    x.lambdaClosure()
    #x.printData()
    x.toNFA()
    #print(x.passed)
    #x.printData()

