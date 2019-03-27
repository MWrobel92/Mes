from os.path import isfile
import numpy
	
class Zadanie:
	def __init__(self):
		self.wspolrzedneWezlow = []
		self.koneksje = []
		self.brzegi = []
		self.obszary = []
		self.liczbaWymiarow = 2
		
		self.macierz = numpy.zeros((0,0))

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
			
		print('Macierz')
		print(self.macierz)
		
			
	def utworz_macierz(self) :
		liczba_wezlow = len(self.wspolrzedneWezlow)
		self.macierz = numpy.zeros((liczba_wezlow, liczba_wezlow))
		
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
						self.macierz[wezel1][wezel2] += a / 6.0
					else :
						self.macierz[wezel1][wezel2] += a / 12.0
		

if __name__ == "__main__":

	mes = Zadanie()
	mes.wczytaj("test.msh")
	mes.utworz_macierz()
	mes.wypisz()