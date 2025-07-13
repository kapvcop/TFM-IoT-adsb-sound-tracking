from utils.config_man import ConfigManager      #llamar a mediador de archivo .json
from math import radians, sin, cos, sqrt, atan2 # Importar funciones matemáticas necesarias para el cálculo de distancias
 #Funcion de calculo de distancia dada mis coordenadas y las reportadas por el avion, con el uso de la fórmula de Haversine:
class CalculadoraDistancias:
    @staticmethod
    def calcular_distancia(lat2, lon2):
        """
        Calcula la distancia en metros entre dos puntos geográficos
        utilizando la fórmula de Haversine.

        Parámetros:
        - Latitud_disp, Longitud_disp: Coordenadas de ubicacion del sensor.
        - lat2, lon2: Coordenadas del rastreo del avion.

        Retorna:
        - Distancia en metros.
        """
        ruta_config = "utils/config.json"                                # Ruta al archivo JSON
        gestor_config = ConfigManager(ruta_config)                       # Cargar la configuración
        Latitud_disp = float(gestor_config.get_param("Latitud","0.0"))   # Obtener Latitud del sensor
        Longitud_disp = float(gestor_config.get_param("Longitud","0.0")) # Obtener Longitud del sensor
#
        # Radio de la Tierra en metros
        R = 6371000  
#
        # Convertir las coordenadas de grados a radianes
        Latitud_disp, Longitud_disp, lat2, lon2 = map(radians, [Latitud_disp, Longitud_disp, lat2, lon2])
#
        # Diferencias entre las coordenadas
        dif_lat = lat2 - Latitud_disp
        dif_lon = lon2 - Longitud_disp
#
        # Fórmula de Haversine
        a = sin(dif_lat / 2)**2 + cos(Latitud_disp) * cos(lat2) * sin(dif_lon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
#
        # Distancia en metros
        distancia = R * c
        return distancia
