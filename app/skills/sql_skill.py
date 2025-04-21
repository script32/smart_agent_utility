from semantic_kernel.functions import kernel_function
from typing import Annotated
from app.plugins.sql_plugin import SqlPlugin


class SqlSkill:
    def __init__(self):
        self.plugin = SqlPlugin()

    @kernel_function(description="Buscar fallas eléctricas por comuna. Si no encuentra, sugiere comunas con fallas recientes.")
    def obtener_fallas_por_comuna_con_fallback(
        self, comuna: Annotated[str, "Nombre de la comuna"]
    ) -> str:
        result = self.plugin.obtener_fallas_por_comuna_con_fallback(comuna)
        return str(result)

    @kernel_function(description="Obtener todas las líneas de transmisión")
    def obtener_lineas(self) -> str:
        result = self.plugin.obtener_lineas_transmision()
        return str(result)

    @kernel_function(description="Obtener todas las comunas")
    def obtener_comunas(self) -> str:
        result = self.plugin.obtener_comunas()
        return str(result)

    @kernel_function(description="Buscar calles desde OpenStreetMap por nombre parcial")
    def buscar_calles(
        self, nombre_parcial: Annotated[str, "Texto parcial del nombre de una calle"]
    ) -> str:
        result = self.plugin.obtener_calles(nombre_parcial)
        return str(result)

    @kernel_function(description="Obtener eventos por línea de transmisión usando su ID")
    def obtener_eventos_por_linea(
        self, id_linea: Annotated[str, "ID de la línea de transmisión"]
    ) -> str:
        try:
            result = self.plugin.obtener_eventos_por_linea(int(id_linea))
            return str(result)
        except ValueError:
            return "El valor de 'id_linea' debe ser un número entero"

    @kernel_function(description="Ejecutar una consulta SQL libre. Solo se permiten SELECT por seguridad.")
    def consulta_sql_libre(
        self, query: Annotated[str, "Consulta SQL completa (solo SELECT)"]
    ) -> str:
        result = self.plugin.consulta_sql_libre(query)
        return str(result)
