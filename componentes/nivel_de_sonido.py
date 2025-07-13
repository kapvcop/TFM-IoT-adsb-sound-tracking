import sounddevice as sd                    # Para manejar la captura de audio 
import numpy as np                          # Para manejar el audio
import threading                            # Para manejar hilos
from utils.config_man import ConfigManager  # Asegúrate de que el módulo esté disponible y bien configurado
#
class MedidorSonido: 
    """ Clase para medir el nivel de sonido en tiempo real """
    def __init__(self, config_path):
        config = ConfigManager(config_path)
        self.device_id = config.get_param("device_id", 1)
        self.samplerate = config.get_param("samplerate", 44100)
        self.channels = config.get_param("channels", 1)
        self.db = 0.0
        self._stop_event = threading.Event()
#
    def _audio_callback(self, indata, frames, time, status):
        """Callback para calcular el nivel de sonido."""
        if status:
            print(status)
        rms = np.sqrt(np.mean(indata**2))
        self.db = 20 * np.log10(rms / 0.00002) if rms > 0 else 0.0
#
    def iniciar_captura(self):
        """Método que corre en un hilo para capturar el sonido en tiempo real."""
        with sd.InputStream(device=self.device_id,
                            samplerate=self.samplerate,
                            channels=self.channels,
                            callback=self._audio_callback):
            while not self._stop_event.is_set():
                sd.sleep(100)
#
    def detener_captura(self):
        """Detiene la captura de sonido."""
        self._stop_event.set()
#
    def obtener_nivel_sonido(self):
        """Devuelve el nivel de sonido actual."""
        return self.db
