from os.path import isfile
from matplotlib import pyplot
import numpy
import re
from Obszar import Obszar

class WarunekBrzegowyIII :
    def __init__(self, w1, w2, temp, alfa, obszar):

        # Indeksy wezlow
        self.w1 = w1
        self.w2 = w2
    
        # Temperatura otoczenia
        self.temp = temp
    
        # Wspolczynnik wymiany ciepla z otoczeniem
        self.alfa = alfa

        # Obszar, na ktorym znajduje sie brzeg
        self.obszar = obszar

class Zadanie:
    def __init__(self):
        self.obszary_obiekty = []

        self.wspolrzedneWezlowWczytane = []
        self.wspolrzedneWezlow = []
        self.koneksje = []
        self.brzegi = []
        self.obszary = []
        self.liczbaWymiarow = 2
        self.liczbaWezlow = 0
        self.liczbaElementow = 0
        self.liczbaBrzegow = 0
        self.liczbaObszarow = 0
        self.warunkiBrzegoweWczytane = []
        self.warunkiBrzegowe = []
        self.warunkiPoczatkowe = []
        # Macierz masowa
        self.macierzM = [[]]    
        # Macierz sztywnosci
        self.macierzK = [[]]
        #Własności materiałowe
        self.wlasnosciMaterialowe = []

        # Aktualna temperatura
        self.T = [[]]
        # Aktualny czas
        self.t = 0


    def wczytaj_msh (self,fname):
        u""" Funkcja do wycztytania danych z pliku mes nazwa pliku bez rozszerzenia"""
        fname = fname + ".msh"
        f = open(fname,"r+")
        lines = f.readlines()
        ilWierszy = len(lines)-1
        i = 0
        while i < ilWierszy:
            j = 0
            if lines[i] == "\n":
                i += 1
                continue
            elif lines[i] == "[LICZBA WYMIAROW]\n":
                self.liczbaWymiarow = int(lines[i+1])
                i += 2
            elif lines[i] == "[LICZBA WEZLOW]\n":
                self.liczbaWezlow = int(lines[i+1])
                i += 2
            elif lines[i] == "[LICZBA ELEMENTOW]\n":
                self.liczbaElementow = int(lines[i+1])
                i += 2			
            elif lines[i] == "[LICZBA BRZEGOW]\n":
                self.liczbaBrzegow = int(lines[i+1])
                i += 2
            elif lines[i] == "[LICZBA OBSZAROW]\n":
                self.liczbaObszarow = int(lines[i+1])
                i += 2
            elif lines[i] == "[WSPOLRZEDNE WEZLOW]\n":
                i += 1
                for j in range(self.liczbaWezlow):
                    row = lines[i+j].split()
                    for k in range(len(row)):
                        row[k] = float(row[k])
                    self.wspolrzedneWezlowWczytane.append(row)
                i = i + self.liczbaWezlow
            elif lines[i] == '[KONEKSJE]\n':
                i = i + 1
                for j in range(ilWierszy-i):
                    if lines[i+j][0] == "[":
                        i += j
                        break
                    elif lines[i+j] == '\n':
                        continue
                    else:
                        row = lines[i+j].split()
                        for k in range(2,len(row)):
                            row[k] = int(row[k])
                        self.koneksje.append(row)
            elif lines[i] == '[BRZEGI]\n':
                i = i + 1
                while j < (ilWierszy-i):
                    if lines[i+j][0] == "[":
                        i += j
                        break
                    elif lines[i+j] == '\n':
                        j += 1
                        continue
                    else:
                        row = lines[i+j].split()
                        row.extend(lines[i+j+1].split())
                        for k in range(len(row)):
                            row[k] = int(row[k])
                        self.brzegi.append(row)
                        j += 3
            elif lines[i] == '[OBSZARY]\n':
                i = i + 1
                koniec = ilWierszy-i-1
                for j in range(koniec):
                    if lines[i+j] == '\n':
                        continue
                    else:
                        row = lines[i+j].split()
                        row.extend(lines[i+j+1].split())
                        for k in range(len(row)):
                            try:
                                row[k] = int(row[k])
                            except:
                                pass
                        self.obszary.append(row)
                        i = i + 1
            else:
                i += 1
        f.close()

    def wypisz_wczytany_msh(self):
        print ('[LICZBA WYMIAROW]: ' , self.liczbaWymiarow)
        print ('[LICZBA WEZLOW]: ' , self.liczbaWezlow)		
        print ('[LICZBA ELEMENTOW]: ' , self.liczbaElementow)		
        print ('[LICZBA BRZEGOW]: ' , self.liczbaBrzegow)	
        print ('[LICZBA OBSZAROW]: ' , self.liczbaObszarow)		
        print ('[WSPOLRZEDNE WEZLOW]: ' ,*self.wspolrzedneWezlowWczytane,sep="\n")
        print ('[KONEKSJE]: ', *self.koneksje, sep="\n")
        print ('[BRZEGI]: ', *self.brzegi, sep="\n")
        print ('[OBSZARY]: ', *self.obszary, sep="\n")

    def weryfikuj_linie_naglowkowa(self,liniaDoAnalizy):
        tmp = liniaDoAnalizy.split()
        if len(tmp) == 5:
            try:
                if int(tmp[0]) == self.liczbaWymiarow and int(tmp[1]) == self.liczbaWezlow and int(tmp[2]) == self.liczbaElementow and int(tmp[3]) == self.liczbaObszarow and int(tmp[4]) == self.liczbaBrzegow :
                    return 1
            except:
                return 0
        else:
            return 1



    def wczytaj_m (self,fname):
        fname += ".m"
        f = open(fname,"r+")
        lines = f.readlines()
        i = 0
        j = 0 
        row = []

        while i < len(lines):
            if lines[i] == "\n":
                i += 1
                continue
            elif not(re.search("^\d",lines[i])):
                i += 1
                continue
            elif lines[i] == '101\n':
                iloscParametrow = int(lines[i+1])
                i += 2
                while j < iloscParametrow:
                    row.append(float(lines[i+1]))
                    i += 3
                    j += 1
                self.wlasnosciMaterialowe.append(row)
                row = []
                j = 0
            else:
                i += 1

    def wczytaj_ic (self,fname):
        fname += ".ic"
        f = open(fname,"r+")
        lines = f.readlines()
        i = 0
        j = 0 
        row = []

        while i < len(lines):
            if lines[i] == "\n":
                i += 1
                continue
            elif not(re.search("^\d",lines[i])):
                i += 1
                continue
            elif lines[i] == '0\n':
                self.warunkiPoczatkowe = lines[i+1].split()
                for j in range(len(self.warunkiPoczatkowe)):
                    self.warunkiPoczatkowe[j] = float(self.warunkiPoczatkowe[j])
                break
            elif self.weryfikuj_linie_naglowkowa(lines[i]):
                i += 1
                continue
            else:
                i += 1

    def wypisz_ic (self):   
        print("[WARUNKI POCZĄTKOWE]")
        print (self.warunkiPoczatkowe)

    def wczytaj_bc (self,fname):
        fname += ".bc"
        f = open(fname,"r+")
        lines = f.readlines()
        i = 0
        j = 0 
        row = []
        tryb = 0
        ilBrzegow = 0
        ilParametrow = 0
        nrBrzegu = 0
        tmp = []

        while i < len(lines):
            if lines[i] == "\n": # pusta linia
                i += 1
                continue
            elif not(re.search("^\d",lines[i])): #omiń tekst i komentarze
                i += 1
                continue
            elif tryb == 1: # porawny plik i wyciągnięta ilość warunków pocz.
                row = lines[i].split()
                if int(row[3]) == 0:
                    i += 2
                    continue
                else:
                    tmp.append(int(row[0])) #nr brzegu
                    i += 1
                    row = lines[i].split()
                    ilParametrow = int(row[3])
                    i += 3
                    for j in range(ilParametrow):
                        tmp.append(float(lines[i]))
                        i += 2
                    self.warunkiBrzegoweWczytane.append(tmp)
                    tmp = []

            elif self.weryfikuj_linie_naglowkowa(lines[i]) and tryb == 0:
                tryb = 1
                ilBrzegow = int(lines[i+2])
                i += 3
                continue
            else:
                i += 1
    def wypisz_bc (self):
        print("[WARUNKI BRZEGOWE]")
        print(self.warunkiBrzegoweWczytane)

    def wypisz_m(self):
        i = 0
        print ("[WARUNKI MATERIAŁOWE]")
        while i < len(self.wlasnosciMaterialowe):
           j = 0
           while j < len(self.wlasnosciMaterialowe[i]):
               if j == 0: print("[" + str(i) + "] Gestosc: " + str(self.wlasnosciMaterialowe[i][j]))
               elif j == 1: print("[" + str(i) + "] Cieplo wlasciwe: " + str(self.wlasnosciMaterialowe[i][j]))
               elif j == 2: print("[" + str(i) + "] Przewodzenie ciepla: " + str(self.wlasnosciMaterialowe[i][j]))
               else: print("[" + str(i) + "] Nieokreślony parametr: " + str(self.wlasnosciMaterialowe[i][j]))
               j += 1
           i += 1

    def zrob_obiekty(self) :
        for ob in self.obszary :
            nowy = Obszar()
            nowy.nazwa = ob[2]
            self.obszary_obiekty.append(nowy)

        # Utworzenie nowej listy wezlow, inaczej indeksowanej
        for wz in self.wspolrzedneWezlowWczytane :
            self.wspolrzedneWezlow.append([wz[1], wz[2]])

        for ob in self.obszary_obiekty :
            ob.wspolrzedneWezlow = self.wspolrzedneWezlow

        for kon in self.koneksje :
            id_obszaru = kon[-1]-1
            self.obszary_obiekty[id_obszaru].koneksje.append([kon[2]-1,kon[3]-1,kon[4]-1])

        for i in range(len(self.obszary_obiekty)) :
            self.obszary_obiekty[i].p = self.wlasnosciMaterialowe[i][0]
            self.obszary_obiekty[i].c = self.wlasnosciMaterialowe[i][1]
            self.obszary_obiekty[i].l = self.wlasnosciMaterialowe[i][2]

        # Tworzenie macierzy, globalne
        liczba_wezlow = len(self.wspolrzedneWezlowWczytane)
        self.macierzM = numpy.zeros((liczba_wezlow, liczba_wezlow))
        self.macierzK = numpy.zeros((liczba_wezlow, liczba_wezlow))

        for ob in self.obszary_obiekty :
            tymczasowaM, tymczasowaK = ob.utworz_macierz()
            self.macierzM += tymczasowaM
            self.macierzK += tymczasowaK

        # Temperatura niech bedzie przechowywana globalnie
        self.T = numpy.zeros((len(ob.wspolrzedneWezlow), 1))
        for i in range(len(self.obszary_obiekty)) :
            for kon in self.obszary_obiekty[i].koneksje :
                self.T[kon[0]] = self.warunkiPoczatkowe[i]
                self.T[kon[1]] = self.warunkiPoczatkowe[i]
                self.T[kon[2]] = self.warunkiPoczatkowe[i]

        #TODO: Wczytac warunki brzegowe z pliku - na razie sa na sztywno
        for wb in self.warunkiBrzegoweWczytane :
            if len(wb) > 2 :
                wezly_brzegu = numpy.add(self.brzegi[wb[0]][3:],-1)
                id_obszaru = self.brzegi[wb[0]][2]-1
                for i in range(0, len(wezly_brzegu)-1, 2) :
                    b = WarunekBrzegowyIII(wezly_brzegu[i], wezly_brzegu[i+1], wb[0], wb[1], self.obszary_obiekty[id_obszaru])
                    self.warunkiBrzegowe.append(b)
        
        #for br in self.brzegi :
        #    id_obszaru = br[2]-1
        #    self.obszary_obiekty[id_obszaru].brzegi.append(numpy.add(br[3:],-1))
        #self.warunkiBrzegowe.append(WarunekBrzegowyIII(423, 424, 300.0, 1000.0, self.obszary_obiekty[0]))
        #self.warunkiBrzegowe.append(WarunekBrzegowyIII(  2,   3, 300.0, 1000.0, self.obszary_obiekty[1]))

    def wypisz_obiekty(self) :
        for ob in self.obszary_obiekty :
            ob.wypisz()
            
    def wyswietl_obiekty(self) :

        pyplot.title('Temperatura po czasie [s]: ' + str(self.t))

        x = []
        y = []
        for w in self.wspolrzedneWezlow :
            x.append(w[0])
            y.append(w[1])

        c = 'r'
        for ob in self.obszary_obiekty :
            if c == 'r' :
                c = 'g'
            else :
                c = 'r'

            for w in ob.koneksje :
                pyplot.plot([x[w[0]], x[w[1]], x[w[2]], x[w[0]]], [y[w[0]], y[w[1]], y[w[2]], y[w[0]] ], '-', c=c)

        pyplot.plot(x, y, 'ob')

        for i in range(len(self.T)) :
            pyplot.text(x[i], y[i], "{:4.3f}".format(self.T[i][0]), size='x-small')

        pyplot.show()


    def wypisz_temp(self) :
        print('Temperatura po czasie [s]' + str(self.t))
        print(self.T)

    def krok(self, dt) :
        # dt - krok czasowy
        self.t += dt
        
        # Uklad rownan w postaci Ax = B
        A = self.macierzM
                   
        MK = self.macierzM - self.macierzK*dt

        # numpy.savetxt("MacierzMK.txt", MK)

        # Uwzglednienie warunkow brzegowych
        brzeg = numpy.zeros((len(self.wspolrzedneWezlow), 1))

        for b in self.warunkiBrzegowe :    
            brzeg[b.w1] += dt * b.alfa * (-2 * self.T[b.w1] - self.T[b.w2] + 3 * b.temp) / (6.0 * b.obszar.c * b.obszar.p)
            brzeg[b.w2] += dt * b.alfa * (-2 * self.T[b.w2] - self.T[b.w1] + 3 * b.temp) / (6.0 * b.obszar.c * b.obszar.p)
        
        B = numpy.matmul(MK, self.T + brzeg)		

        x = numpy.linalg.solve(A, B)
        self.T = x