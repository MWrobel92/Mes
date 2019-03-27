from os.path import isfile
import numpy
	
class Zadanie:
	def __init__(self):
		self.wspolrzedneWezlow = []
		self.koneksje = []
		self.brzegi = []
		self.obszary = []
		self.liczbaWymiarow = 2
		
		# Macierz masowa
		self.macierzM = [[]]	
		# Macierz sztywnosci
		self.macierzK = [[]]

		#TODO: Ponizsze wartosci powinny byc wczytywane z pliku
		
		# Gestosc
		self.p = 7.700000e+003
		# Cieplo wlasciwe
		self.c = 8.000000e+002
		# Przewodzenie ciepla
		self.l = 4.000000e+001
		
		# Aktualna temperatura
		self.T = [[]]
		
		# Aktualny czas
		self.t = 0

	def wczytaj(self,plik): 
	
		tryb = 0
		f = open(plik, "r+")
		for l in f:
			if (l == '[WSPOLRZEDNE WEZLOW]\n'):
				tryb = 1
			elif (l == '[KONEKSJE]\n'):
				tryb = 2    
			elif (l == '[BRZEGI]\n'):
				tryb = 3  
				
			elif (tryb == 1) :
				if ( l=='\n') : 
					tryb = 0
				else:
					t = l.split("  ")
					tmp = [float(t[1]), float(t[2])]
					self.wspolrzedneWezlow.append(tmp)
					
			elif (tryb == 2) :
				if (l=='\n') : 
					tryb = 0
				else:
					t = l.split(" ")
					# Odejmujemy jedynke, zeby numery indekow sie zgadzaly
					tmp = [int(t[2])-1, int(t[3])-1, int(t[4])-1]
					self.koneksje.append(tmp)
					
			elif (tryb == 3) :
				if (l=='\n') : 
					tryb = 0
				else:
					tryb = 4
				
			elif (tryb == 4) :
				if (l=='\n') : 
					tryb = 3
				else:
					t = l.split(" ")
					# Odejmujemy jedynke, zeby numery indekow sie zgadzaly
					tmp = [int(t[0])-1, int(t[1])-1]
					self.brzegi.append(tmp)
					
	def wczytaj_warunki_poczatkowe(self,plik) :
		#TODO: Wczytac warunki poczatkowe z pliku - na razie sa na sztywno
		self.T = numpy.zeros((len(self.wspolrzedneWezlow), 1))
		self.T += 600.0
					
	def wypisz(self) :
		print('Wezly')
		for w in self.wspolrzedneWezlow :
			print(w)
		
		print('Koneksje')
		for w in self.koneksje :
			print(w)
		
		print('Brzegi')
		for w in self.brzegi :
			print(w)
			
		print('Macierz masowa')
		print(self.macierzM)
		
		print('Macierz sztywnosci')
		print(self.macierzM)
		
			
	def utworz_macierz(self) :
		liczba_wezlow = len(self.wspolrzedneWezlow)
		self.macierzM = numpy.zeros((liczba_wezlow, liczba_wezlow))
		self.macierzK = numpy.zeros((liczba_wezlow, liczba_wezlow))
		
		for obszar in self.koneksje :
			# Pole obszaru - ze wzoru na pole trojkata o danych wierzcholkach
			a1 = self.wspolrzedneWezlow[obszar[0]][0]
			a2 = self.wspolrzedneWezlow[obszar[0]][1]
			b1 = self.wspolrzedneWezlow[obszar[1]][0]
			b2 = self.wspolrzedneWezlow[obszar[1]][1]
			c1 = self.wspolrzedneWezlow[obszar[2]][0]
			c2 = self.wspolrzedneWezlow[obszar[2]][1]
			a = numpy.abs(a1*b2+b1*c2+c1*a2-c1*b2-a1*c2-b1*a2) / 2.0
			
			for wezel1 in obszar :
				for wezel2 in obszar :
					if (wezel1 == wezel2) :
						self.macierzM[wezel1][wezel2] += a / 6.0
					else :
						self.macierzM[wezel1][wezel2] += a / 12.0
						
					#TODO: Wypelnic takze macierzK
					
	
						
	def krok(self, dt) :
		# dt - krok czasowy
		self.t += dt
		
		# Uklad rownan w postaci Ax = B
		A = self.macierzM
				
		a = self.l / (self.c * self.p)		
		MK = self.macierzM - (self.macierzK*a*dt)		
		B = numpy.matmul(MK, self.T)

		x = numpy.linalg.solve(A, B)
		self.T = x
		
		print("Temperatura po czasie " + str(self.t))
		print(self.T)

if __name__ == "__main__":

	mes = Zadanie()
	mes.wczytaj("test.msh")
	mes.wczytaj_warunki_poczatkowe("test.ic")
	mes.utworz_macierz()	
	mes.wypisz()
	
	mes.krok(0.1)