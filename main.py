from utils.config_man import ConfigManager
from componentes.capturador_dump1090 import CapturadorDump1090
from componentes.seguidor_de_avion import SeguidorDeAvion
from componentes.nivel_de_sonido import MedidorSonido
from componentes.cliente_aws_iot import AWSIoTClient
from utils.logger_util import LoggerUtil
from datetime import datetime
import threading
#
#  Funcion para tomar el serial del equipo  para individualizar cada equipo que se conecte al AWS, especialmente al colocar más dispositivos.
def obtener_numero_serie():
    with open("/proc/cpuinfo", "r") as f:
        for line in f:
            if line.startswith("Serial"):
                return line.strip().split(":")[1].strip()
    return None

def main():
#
    # Configuración inicial de los modulos
    print(" Iniciando entorno ")
    raspb_numero_serie = obtener_numero_serie()                        # Obtener el serial del equipo
    ruta_config = "utils/config.json"                                  # Ruta al archivo JSON
    gestor_config = ConfigManager(ruta_config)                         # Instancia del gestor de configuración
    ruta_dump1090 = gestor_config.get_param("ruta_dump1090","/")       # Configurar la dirección del Dump1090
    altura_in = gestor_config.get_param("altura_det")                  # Altura de detección inicial
    altura_fin = gestor_config.get_param("altura_fin")                 # Altura de detección final
    distancia_ini = gestor_config.get_param("distancia_inicial")       # Obtener parametro Dist inicial
    distancia_fin = gestor_config.get_param("distancia_final")         # Obtener parámetro Dist Final
    tiempo_inactividad = gestor_config.get_param("tiempo_inactividad") # Tiempo de inactividad para el seguidor
    logger = LoggerUtil(log_file="log_sistema.log")                    # Configurar el logger
#
    #----------- Datos para la configuración de la conexión con AWS --------------------------------
    #  No he incluído los certificados de seguridad, considerando que son privados y deben ser gestionados de forma segura.
    #  Dejo los nombres de los archivos de certificados para que el usuario los coloque en la carpeta "certificados" del proyecto.
    #----------------------------------------------------------------------------------------------
    endpoint = "a2gklyg60jp582-ats.iot.us-east-1.amazonaws.com" 
    cert_path = "certificados/device-certificate.pem.crt" 
    key_path = "certificados/private.pem.key" 
    ca_path = "certificados/AmazonRootCA1.pem" 
    topic ="sensorlvl"
    #------------------------------------------------------------------------------------------------    
#
    #Iniciar proceso de captura de sonido
    medidor_sonido = MedidorSonido(config_path=ruta_config)
    hilo_sonido = threading.Thread(target=medidor_sonido.iniciar_captura, daemon=True)
    hilo_sonido.start()
    #----------------------------
    print(" Iniciando entorno MQTT ")
    #inicializar entorno MQTT
    clientaws = AWSIoTClient(endpoint, cert_path, key_path, ca_path, topic, raspb_numero_serie)
    clientaws.conectar()
    clientaws.suscribirse()
#
    print(" Iniciando seguidor de Avión ")
    seguidor = SeguidorDeAvion(tiempo_inactividad, distancia_ini, distancia_fin, medidor_sonido, logger, clientaws)
#
    # Inicializamos el capturador y comenzamos la captura
    capturador = CapturadorDump1090(ruta_dump1090, seguidor, altura_in, altura_fin, medidor_sonido)
    print(" ") 
    print(f" Iniciando captura desde dump1090..., altura de detección: {altura_in} Raspberry PI 3 SN: {raspb_numero_serie}")
    print(" Fecha y hora de inicio: ", datetime.now())
    print(" ")
    try:
        print("-Iniciar captura-")
        capturador.iniciar_captura()
      #  print("-Captura iniciada-")
        medidor_sonido.detener_captura()
        clientaws.desconectar() 
    except KeyboardInterrupt:
        print("Finalizando programa...")
        seguidor.mostrar_seguimientos()  # Mostrar historial completo


if __name__ == "__main__":
    main()
