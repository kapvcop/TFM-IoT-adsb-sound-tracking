import subprocess                      # Para ejecutar el programa dump1090
import re                              # Para manejar expresiones regulares
import time                            # Para manejar tiempos
from componentes.avion import Avion    # Importar la clase Avion
#
class CapturadorDump1090:
    def __init__(self, ruta_dump1090, seguidor, altura_in, altura_fin, medidor_sonido):
        self.ruta_dump1090 = ruta_dump1090 # Ruta al ejecutable de dump1090
        self.seguidor = seguidor           # Instancia del seguidor de aviones
        self.sonido = medidor_sonido       # Instancia del medidor de sonido
        self.alt_in = altura_in            # Altura a la que comienza a hacersele seguimientto al avion
        self.alt_fin = altura_fin          # Altura a la que se le deja dejacer seguimiento al avion
        self.msg_pattern = re.compile(     # Expresión regular para capturar los datos del dump1090
            r"([0-9a-fA-F]{6})\s+(\S{0,8})\s+(-?\d+)\s+(\d+)\s+([-+]?\d+\.\d+)\s+([-+]?\d+\.\d+)\s+(\d+)\s+(\d+)\s+(\d+\s+sec)"
        )
#
    def iniciar_captura(self):
        """
        Inicia el proceso de captura del dump1090 y filtra en tiempo real los aviones detectados.
        """
        with subprocess.Popen([self.ruta_dump1090, '--interactive'], stdout=subprocess.PIPE, text=True) as proc:
            try:
                for line in proc.stdout:
                    #print(f"-Search match- Sonido {self.sonido.obtener_nivel_sonido()}")     # si quieres hacer debug del sonido
                    match = self.msg_pattern.search(line)
                    if match:
                        hex_code = match.group(1)                           # Identificador del transponder
                        ultimo_msgv = int(match.group(9).split()[0])        # Extrae el valor de 'seen' en segundos
                        flight = match.group(2) if match.group(2) else "0"  # hsi viene vacio lo hacemos 0 para anularlo
                        
                        avion = Avion(                                       # Crear una instancia de Avion con los datos capturados
                            matricula=hex_code,                              # Identificador del transponder unico 
                            vuelo=flight,                                    # Identificador de vuelo
                            altura=int(match.group(3)),                      # Altura del vuelo
                            velocidad=int(match.group(4)),                   # Velocidad del vuelo
                            latitud=float(match.group(5)),                   # Latitud
                            longitud=float(match.group(6)),                  # Longitud
                            tiempo_visto=time.time(),                        # Momento de visualización
                            ultimo_msgv=ultimo_msgv,                         # Ultimo mensaje detectado
                            sonido = self.sonido.obtener_nivel_sonido()      # Sonido inicial
                        )
#                       
                        # Solo procesa los aviones que cumplen las condiciones
                        #
                        if ( ((avion.altura <= self.alt_in) and (avion.altura >= self.alt_fin) ) and (flight != "0")):
                            # este print es para debug, si quieres ver los aviones que se capturan ***
                            print(f"AAA> -6- Vuelo: {avion.vuelo} Matricula: {avion.matricula} Altura DETC: {avion.altura} Velocidad DETC: {avion.velocidad} Latitud: {avion.latitud} Long: {avion.longitud} Seen: {avion.ultimo_msgv}")
                            self.seguidor.actualizar_seguimientos([avion])
                        #else:
                           # print(f"BBB> Vuelo: {avion.vuelo} Matricula: {avion.matricula} Altura DETC: {avion.altura} Velocidad DETC: {avion.velocidad} Latitud: {avion.latitud} Long: {avion.longitud} Seen: {avion.ultimo_msgv}")
#
            except KeyboardInterrupt:
                print("\nCaptura interrumpida por el usuario.")
            finally:
                proc.terminate()
