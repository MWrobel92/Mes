from os.path import isfile
import numpy

class Obszar :

	def __init__(self):
		self.wspolrzedneWezlow = []
		self.koneksje = []
		self.brzegi = []
		self.liczbaWymiarow = 2
		self.nazwa = "untitled"
		
		self.warunkiBrzegowe = []
		
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
		
	def utworz_macierz(self) :
		liczba_wezlow = len(self.wspolrzedneWezlow)
		self.macierzM = numpy.zeros((liczba_wezlow, liczba_wezlow))
		self.macierzK = numpy.zeros((liczba_wezlow, liczba_wezlow))
		
		# Przepisanie wspolrzednych do osobnych tablic, zeby kod byl bardziej czytelny
		x = []
		y = []
		for wezel in self.wspolrzedneWezlow :
			x.append(wezel[0])
			y.append(wezel[1])

		
		for obszar in self.koneksje :
			# Pole obszaru - ze wzoru na pole trojkata o danych wierzcholkach
			a1 = x[obszar[0]]
			a2 = y[obszar[0]]
			b1 = x[obszar[1]]
			b2 = y[obszar[1]]
			c1 = x[obszar[2]]
			c2 = y[obszar[2]]
			a = numpy.abs(a1*b2+b1*c2+c1*a2-c1*b2-a1*c2-b1*a2) / 2.0        
			
			for wezel1 in obszar :
				for wezel2 in obszar :
					# Robimy macierz "lumped". Gdyby to była ta zwykla, to byloby "a / 6.0" i "a / 12.0"
					if (wezel1 == wezel2) :
						self.macierzM[wezel1][wezel2] += a / 12.0
					else :
						self.macierzM[wezel1][wezel2] += 0
						
			for i in range(len(obszar)) :
				for j in range(len(obszar)) :
					# i oraz j to wspolrzedne lokalne (0, 1, 2)
					
					# Dla i oraz j trzeba znalezc indeksy sasiednich wezlow
					# Przykladowo, jesli i = 2, to i_m_1 = 1 a  i+1 = 0 (bo doszlismy do konca tablicy) 
					i_p_1 = (i+1) % len(obszar)                 
					i_m_1 = i-1
					if i_m_1 < 0 :
						i_m_1 = len(obszar)-1
						
					j_p_1 = (j+1) % len(obszar)
					j_m_1 = j-1
					if j_m_1 < 0 :
						j_m_1 = len(obszar)-1                       
						
					# Obliczamy wartosci C
					c2i = y[obszar[i_p_1]] - y[obszar[i_m_1]]
					c2j = y[obszar[j_p_1]] - y[obszar[j_m_1]]
					
					c3i = x[obszar[i_m_1]] - x[obszar[i_p_1]]           
					c3j = x[obszar[j_m_1]] - x[obszar[j_p_1]]
					
					#Wypelniamy macierzK
					self.macierzK[obszar[i]][obszar[j]] += (c2i*c2j + c3i*c3j) / (4.0 * a)              
	
						
	def krok(self, dt) :
		# dt - krok czasowy
		self.t += dt
		
		# Uklad rownan w postaci Ax = B
		A = self.macierzM
				
		a = self.l / (self.c * self.p)      
		MK = self.macierzM - (self.macierzK*a*dt)
		
		# Uwzglednienie warunkow brzegowych
		brzeg = numpy.zeros((len(self.wspolrzedneWezlow), 1))
		
		for b in self.warunkiBrzegowe :    
			brzeg[b.w1] += dt * b.alfa * (-2 * self.T[b.w1] - self.T[b.w2] + 3 * b.temp) / (6.0 * self.c * self.p)
			brzeg[b.w2] += dt * b.alfa * (-2 * self.T[b.w2] - self.T[b.w1] + 3 * b.temp) / (6.0 * self.c * self.p)
		
		B = numpy.matmul(MK, self.T + brzeg)		

		x = numpy.linalg.solve(A, B)
		self.T = x
		
	def wypisz(self) :
		print("== OBSZAR " + self.nazwa + " ==")
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
		print(self.macierzK)

class WarunekBrzegowyIII :
	def __init__(self, w1, w2, temp, alfa):
	
		# Indeksy wezlow
		self.w1 = w1
		self.w2 = w2
		
		# Temperatura otoczenia
		self.temp = temp
		
		# Wspolczynnik wymiany ciepla z otoczeniem
		self.alfa = alfa
	
class Zadanie:

	def __init__(self):
		self.obszary = []
		self.t = 0

	def wczytaj(self,plik):

		obszar = Obszar()
	
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
					obszar.wspolrzedneWezlow.append(tmp)
					
			elif (tryb == 2) :
				if (l=='\n') : 
					tryb = 0
				else:
					t = l.split(" ")
					# Odejmujemy jedynke, zeby numery indekow sie zgadzaly
					tmp = [int(t[2])-1, int(t[3])-1, int(t[4])-1]
					obszar.koneksje.append(tmp)
					
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
					obszar.brzegi.append(tmp)
					
		self.obszary.append(obszar)
					
	def wczytaj_warunki_poczatkowe(self,plik) :
		#TODO: Wczytac warunki poczatkowe z pliku - na razie sa na sztywno
		self.obszary[0].T = numpy.zeros((len(self.obszary[0].wspolrzedneWezlow), 1))
		self.obszary[0].T += 600.0
		
		#self.T[0] = self.T[1]  = 300.0
		
	def wczytaj_warunki_brzegowe(self, plik) :
		#TODO: Wczytac warunki brzegowe z pliku - na razie sa na sztywno
		b = WarunekBrzegowyIII(3, 4, 300.0, 1000.0)
		self.obszary[0].warunkiBrzegowe.append(b)
		
	def utworz_macierze(self):
		for obszar in self.obszary :
			obszar.utworz_macierz()
			
	def wypisz_temp(self) :
		for obszar in self.obszary :
			print(obszar.T)
					
	def wypisz(self) :
		for obszar in self.obszary :
			obszar.wypisz()
		
	def krok(self, dt) :
		self.t += dt
		for obszar in self.obszary :
			obszar.krok(dt)
			


if __name__ == "__main__":

	mes = Zadanie()
	mes.wczytaj("test.msh")
	mes.wczytaj_warunki_poczatkowe("test.ic")
	mes.wczytaj_warunki_brzegowe("test.bc")
	mes.utworz_macierze()    
	mes.wypisz()
	
	for i in range(1000) :
		mes.krok(1)
	
	print("Temperatura po czasie " + str(mes.t) + " s")
	mes.wypisz_temp()