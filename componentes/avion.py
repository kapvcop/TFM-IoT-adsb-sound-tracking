class Avion:
    def __init__(self, matricula, vuelo, altura, velocidad, latitud, longitud, tiempo_visto, ultimo_msgv, sonido=None ):
        self.matricula = matricula          # Identificador Transponder del avión
        self.vuelo = vuelo                  # Identificador del vuelo
        self.altura = altura                # Identificador de la altura
        self.velocidad = velocidad          # Identificador de la velocidad
        self.latitud = latitud              # Identificador de la latitud
        self.longitud = longitud            # Identificador de la longitud
        self.tiempo_visto = tiempo_visto    # Identificador momento de la identificacion
        self.ultimo_msgv = ultimo_msgv      # Tiempo desde el último mensaje detectado
        self.sonido = sonido                # Nivel de sonido registrado
        self.historial = []                 # Historial para registrar cambios

    def actualizar(self, altura, velocidad, latitud, longitud, tiempo_visto, ultimo_msgv, vuelo=None, sonido=None):
        # Registra un cambio solo si la altura o el identificador de vuelo cambian
        if self.altura != altura or (vuelo and vuelo != self.vuelo):
            self.historial.append({
                "altura": altura,
                "velocidad": velocidad,
                "latitud": latitud,
                "longitud": longitud,
                "tiempo_visto": tiempo_visto,
                "ultimo_msgv": ultimo_msgv,
                "vuelo": self.vuelo,  # Registrar el vuelo actual antes de actualizar
                "sonido": self.sonido
            })
        self.altura = altura
        self.velocidad = velocidad
        self.latitud = latitud
        self.longitud = longitud
        self.tiempo_visto = tiempo_visto
        self.ultimo_msgv = ultimo_msgv
        if vuelo:
            self.vuelo = vuelo  # Actualiza el identificador de vuelo si se proporciona uno nuevo
        if sonido is not None:
            self.sonido=sonido 


    def mostrar_historial(self): # Muestra el historial de cambios por motivos de depuración, puede omitirse en producción
        print(f"Seguimiento de {self.matricula} (Vuelo: {self.vuelo}):")
        for cambio in self.historial:
            print(cambio)

