import json                       # Importar el módulo JSON para manejar archivos de configuración
import ssl                        # Importar el módulo SSL para manejar la seguridad de la conexión
import paho.mqtt.client as mqtt   # Importar la librería Paho MQTT para manejar la comunicación MQTT
#
#
class AWSIoTClient:
    def __init__(self, endpoint, cert_path, key_path, ca_path, topic, raspb_numero_serie):
        """
        Inicializa el cliente MQTT para conectarse a AWS IoT.

        :param endpoint: Dirección del endpoint de AWS IoT.
        :param cert_path: Ruta al certificado del cliente.
        :param key_path: Ruta a la clave privada del cliente.
        :param ca_path: Ruta al certificado de la autoridad certificadora (CA).
        :param topic: Tópico MQTT para publicar y suscribirse.
        """
        self.endpoint = endpoint
        self.cert_path = cert_path
        self.key_path = key_path
        self.ca_path = ca_path
        self.topic = topic
        self.raspb_serie = raspb_numero_serie
#
        # Crear el cliente MQTT
        # Creo el Cliente MQTT con un nombre + el serial unico del equipo asi aseguramos que la identidad del cliente MQTT no se repita
        self.client = mqtt.Client(client_id="iot-snd-lvl-"+raspb_numero_serie)
#        
        # Configurar TLS con los certificados proporcionados
        self.client.tls_set(
            ca_certs=self.ca_path,
            certfile=self.cert_path,
            keyfile=self.key_path,
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLSv1_2
        )
        self.client.keepalive = 60
        # Configurar el manejador de mensajes
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
#
    def conectar(self):
        """
        Conecta el cliente MQTT al broker AWS IoT.
        """
        try:
            self.client.connect(self.endpoint, port=8883)
            print(f" Conectado exitosamente a AWS IoT Core en {self.endpoint} ")
            # Mantener el cliente corriendo en un hilo
            self.client.loop_start()
        except Exception as e:
            raise ConnectionError(f" No se pudo conectar a AWS IoT Core: {e} ")

    def publicar_datos(self, datos):
        """
        Publica un mensaje en el tópico configurado.

        :param datos: Diccionario con los datos a publicar.
        """
        try:
            mensaje = json.dumps(datos)
            self.client.publish(self.topic, mensaje)
            print(f" Datos publicados en {self.topic}: {mensaje} ")
        except Exception as e:
            print(f"Error al publicar datos: {e}")

    def suscribirse(self):
        """
        Se suscribe al tópico configurado.
        """
        try:
            self.client.subscribe(self.topic)
            print(f" Suscrito exitosamente al tópico {self.topic} ")
        except Exception as e:
            print(f"Error al suscribirse al tópico: {e}")

    def on_message(self, client, userdata, message):
        """
        Manejador para procesar mensajes recibidos del tópico.

        :param client: Cliente MQTT.
        :param userdata: Información adicional del usuario.
        :param message: Mensaje recibido.
        """
        print(f"Mensaje recibido en {message.topic}: {message.payload.decode('utf-8')}")

    def on_connect(self, client, userdata, flags, rc):
        """
        Callback al conectarse al broker.
        """
        if rc == 0:
            print("Conexión exitosa a AWS IoT Core.")
        else:
            print(f"Error en la conexión: Código {rc}")

    def on_disconnect(self, client, userdata, rc):
        print(f"Desconectado de AWS IoT Core. Código de retorno: {rc}")
        if rc != 0:
           print("La desconexión fue inesperada. Intentando reconectar...")
           self.client.reconnect()

    def desconectar(self):
        """
        Desconecta el cliente MQTT.
        """
        self.client.loop_stop()
        self.client.disconnect()
        print(" Cliente desconectado de AWS IoT Core. ")
