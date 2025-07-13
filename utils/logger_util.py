import logging  # Importar el módulo de logging para manejar los registros
import os       # Importar el módulo os para manejar archivos y directorios

class LoggerUtil:
    def __init__(self, log_file, log_level=logging.DEBUG):
        """
        Inicializa el registro de logs.
        
        :param log_file: Nombre del archivo donde se guardarán los logs.
        :param log_level: Nivel de log (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        """
        if not log_file:
            raise ValueError("Debes proporcionar un nombre para el archivo de logs.")
        
        self.log_file = log_file

        # Configuración básica del logger
        self.logger = logging.getLogger(log_file)  # Usa un nombre específico para evitar conflictos entre loggers
        self.logger.setLevel(log_level)

        # Archivo de logs
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        self.logger.addHandler(file_handler)

        # Salida en consola (opcional)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        self.logger.addHandler(console_handler)

    def debug(self, message):
        """Registra un mensaje con nivel DEBUG."""
        self.logger.debug(message)

    def info(self, message):
        """Registra un mensaje con nivel INFO."""
        self.logger.info(message)

    def warning(self, message):
        """Registra un mensaje con nivel WARNING."""
        self.logger.warning(message)

    def error(self, message):
        """Registra un mensaje con nivel ERROR."""
        self.logger.error(message)

    def critical(self, message):
        """Registra un mensaje con nivel CRITICAL."""
        self.logger.critical(message)

    def clear_log_file(self):
        """Elimina el contenido del archivo de logs."""
        if os.path.exists(self.log_file):
            with open(self.log_file, "w"):
                pass  # Simplemente reescribimos el archivo vacío
