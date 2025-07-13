import json                       # Importar el módulo JSON para manejar archivos de configuración
from typing import Any, Optional  # Importar tipos para anotaciones de tipo

class ConfigManager:
    def __init__(self, ruta_archivo: str):
        self.ruta_archivo = ruta_archivo
        self.datos = self._cargar_json()

    def _cargar_json(self) -> dict:
        try:
            with open(self.ruta_archivo, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: No se encuentra el archivo JSON en: {self.ruta_archivo}.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: No se pudo decodificar el archivo JSON en: {self.ruta_archivo}.")
            return {}
#
    def get_param(self, clave: str, defecto: Optional[Any] = None) -> Any:
        """
        Obtiene un parámetro del JSON. Si no existe, devuelve el valor por defecto proporcionado.
        """
        return self.datos.get(clave, defecto)
#
    def set_param(self, clave: str, valor: Any) -> None:
        """
        Establece un parámetro en el JSON y guarda los cambios.
        """
        self.datos[clave] = valor
        self._guardar_json()
#
    def _guardar_json(self) -> None:
        try:
            with open(self.ruta_archivo, "w") as file:
                json.dump(self.datos, file, indent=4)
        except IOError:
            print(f"Error: No se pudo escribir en el archivo JSON {self.ruta_archivo}.")


