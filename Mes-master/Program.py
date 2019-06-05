from os.path import isfile
import numpy
import re
import mes			

if __name__ == "__main__":
    nazwaProjektu = "htr_1"
    #nazwaProjektu = input("Wprowadź nazwę projektu [default test]")
    zad = mes.Zadanie()
    zad.wczytaj_msh(nazwaProjektu)
    #zad.wypisz_wczytany_msh()
    zad.wczytaj_m(nazwaProjektu)
    zad.wypisz_m()
    zad.wczytaj_ic(nazwaProjektu)
    zad.wypisz_ic()
    zad.wczytaj_bc(nazwaProjektu)
    #zad.wypisz_bc()
    zad.zrob_obiekty()
    #zad.wypisz_obiekty()
    zad.wyswietl_obiekty()
    #zad.wypisz_temp()

    for i in range(50) :
        zad.krok(0.1)

    zad.wyswietl_obiekty()

    for i in range(1150) :
        zad.krok(0.1)

    zad.wyswietl_obiekty()
    #zad.wypisz_temp()
