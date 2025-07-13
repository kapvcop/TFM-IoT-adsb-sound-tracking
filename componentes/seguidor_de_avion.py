from componentes.avion import Avion                         # Importamos la clase Avion 
from utils.calcular_distancia import CalculadoraDistancias  # Calculador de distancias
from datetime import datetime                               # Para manejar fechas y horas
import time                                                 # Para manejar tiempos
#
#
class SeguidorDeAvion:
    def __init__(self, tiempo_maximo_inactividad, distancia_ini, distancia_fin, medidor_sonido, logger, clientaws):
        """Inicializa el seguidor con parámetros configurables."""
        self.aviones_seguidos = {}  # Diccionario para almacenar aviones seguidos (clave: matrícula)
        self.tiempo_maximo_inactividad = tiempo_maximo_inactividad # Tiempo máximo de inactividad para un avión antes de eliminarlo
        self.dist_ini = distancia_ini   # Distancia de Inicio de seguimiento
        self.dist_fin = distancia_fin   # Distancia Final de seguimiento (recordamos que el avion se mueve se acerca "desde" y se aleja "hasta")
        self.sonido = medidor_sonido    # Para Obtener el nivel de sonido en ambiente
        self.logger = logger            # Para llevar control de la aplicacion
        self.clientaws = clientaws      # Para transmitir los datos del avion seguido a IoT-AWS
#
    def actualizar_seguimientos(self, aviones_detectados):
        """Actualiza el seguimiento con los datos de aviones detectados."""
        tiempo_actual = time.time()  #Sin formato
        #tiempo_actual = datetime.fromtimestamp(time.time()).strftime('%d/%m/%Y %H:%M:%S') #Con Formato
#
        # Procesar cada avión detectado
        for avion in aviones_detectados:  # aviones_detectados contiene instancias de `Avion`
            if not isinstance(avion, Avion):
                raise ValueError("Se esperaba un objeto de tipo 'Avion'.")
#
            # Calcular la distancia del avión detectado
            distancia =round(CalculadoraDistancias.calcular_distancia(avion.latitud, avion.longitud),2) #Obtener distancia del Avión
            sonido_medido = self.sonido.obtener_nivel_sonido()                                          #Del medidor de sonido
            # Verificar que esté dentro de los rangos configurados
            if not (self.dist_fin <= distancia <= self.dist_ini):
                self.logger.debug(
                    f"> Avión {avion.vuelo} fuera de rango. Altura: {avion.altura}, "
                    f"Distancia: {distancia:.2f} m."
                )                
                continue
#
            if avion.matricula in self.aviones_seguidos:
                # Actualizar información del avión ya seguido
                avion_seguido = self.aviones_seguidos[avion.matricula]
                avion_seguido.actualizar(
                    altura=avion.altura,            # Altura del vuelo
                    velocidad=avion.velocidad,      # Velocidad del vuelo
                    latitud=avion.latitud,          # Latitud
                    longitud=avion.longitud,        # Longitud
                    tiempo_visto=tiempo_actual,     # Momento de visualización
                    ultimo_msgv=avion.ultimo_msgv,  # Ultimo Mensaje
                    vuelo=avion.vuelo,              # Identificador de vuelo
                    sonido=sonido_medido            # Nivel de Sonido registrado
                )
                mensaje = {
                 "Matricula Transponder: ": avion.matricula,
                 "Vuelo: ": avion.vuelo,
                 "Altura: ": avion.altura,
                 "Velocidad: ": avion.velocidad,
                 "Latitud: ": avion.latitud,
                 "Longitud: ": avion.longitud,
                 "Tiempo: ": datetime.fromtimestamp(avion.tiempo_visto).strftime('%d/%m/%Y %H:%M:%S'),
                 "Nivel sonido: ": round(float(avion.sonido),2),
                 "Distancia del Vuelo ":distancia
                }
                self.clientaws.publicar_datos(mensaje)
                self.logger.debug(f"--> Actualización de seguimiento para vuelo: {mensaje}") # se puede comentar en producción  
               # Si el avión no está en seguimiento, agregarlo             
            else:
                # Agregar un nuevo avión al seguimiento
                self.aviones_seguidos[avion.matricula] = avion
                self.logger.debug(
                    f">> Inicio de seguimiento para vuelo: {avion.vuelo}, " 
                    f"matrícula: {avion.matricula}. Altura: {avion.altura}, "
                    f"Distancia: {distancia:.2f} m. Sonido {sonido_medido}"
                )               
        # Limpiar aviones que ya no están activos
        self._limpiar_aviones_inactivos()#tiempo_actual)

    def _limpiar_aviones_inactivos(self):
     """
     Elimina aviones que no cumplen con los criterios:
     - `ultimo_msgv` llega a 60 (indica que el avión dejó de transmitir).
     - El avión está fuera del rango de distancia permitido.
     """
     matriculas_a_eliminar = []

     for matricula, avion in self.aviones_seguidos.items():
         # Eliminar si `ultimo_msgv` indica que dejó de transmitir
         if avion.ultimo_msgv == 60:
             self.logger.debug(f">>> El vuelo {avion.vuelo}, matrícula {matricula} dejó de transmitir (ultimo_msgv=60).")
             matriculas_a_eliminar.append(matricula)
        
         # Eliminar si está fuera del rango de distancia
         elif not (self.dist_fin <= CalculadoraDistancias.calcular_distancia(avion.latitud, avion.longitud) <= self.dist_ini):
             self.logger.debug(f">>> El vuelo {avion.vuelo}, matrícula {matricula} está fuera de rango.")
             matriculas_a_eliminar.append(matricula)

     # Eliminar los aviones marcados
     for matricula in matriculas_a_eliminar:
         avion = self.aviones_seguidos.pop(matricula)
         self.logger.info(f"El vuelo {avion.vuelo}, matrícula {matricula}, ha sido eliminado del seguimiento.")
 
    def mostrar_seguimientos(self):
        """
        Muestra los historiales de todos los aviones actualmente seguidos.
        """
        for avion in self.aviones_seguidos.values():
            print(f"Historial de vuelo {avion.vuelo}, matrícula {avion.matricula}:")
            avion.mostrar_historial()
