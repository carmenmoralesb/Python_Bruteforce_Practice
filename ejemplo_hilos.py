import threading

#L**E YOU IVAR


class Mi_hilo(threading.Thread):
    def __init__(self,n, target):
        # Recibe los atributos de este hilo
        self.n = n
        self.target = target
        # Inicializa flag de finalización del hilo
        self.final = False
        # Inicializa el Thread
        threading.Thread.__init__(self)

    # Este método sustituye al target del Thread
    def run(self):
        # Código que ejecuta cada hilo
        while True:
            if self.final:
                return
            fin = input(f"Hilo {self.n} {self.target} Final???")
            if fin=="f":
                # Para los demás hilos
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
    
# Lista de hilos
hilos = []
mitarget = "Hooolaaa"
# Crea los hilos
for i in range(0,3):
     hilos.append(Mi_hilo(i, mitarget))
# Inicia los hilos
for hilo in hilos:
    hilo.start(hilos)