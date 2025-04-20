from semantic_kernel import kernel_function, kernel_function_context_parameter
from app.plugins.sql_plugin import SqlPlugin


class SqlSkill:
    def __init__(self):
        self.plugin = SqlPlugin()

    @kernel_function(
        description="Obtener fallas eléctricas recientes por comuna en los últimos 7 días"
    )
    @kernel_function_context_parameter(name="comuna", description="Nombre de la comuna")
    def obtener_fallas_recientes(self, comuna: str) -> str:
        result = self.plugin.obtener_fallas_recientes(comuna)
        return str(result)

    @kernel_function(
        description="Obtener todas las líneas de transmisión"
    )
    def obtener_lineas(self) -> str:
        result = self.plugin.obtener_lineas_transmision()
        return str(result)

    @kernel_function(
        description="Obtener todas las comunas"
    )
    def obtener_comunas(self) -> str:
        result = self.plugin.obtener_comunas()
        return str(result)

    @kernel_function(
        description="Buscar calles desde OpenStreetMap por nombre parcial"
    )
    @kernel_function_context_parameter(name="nombre_parcial", description="Texto parcial del nombre de una calle")
    def buscar_calles(self, nombre_parcial: str) -> str:
        result = self.plugin.obtener_calles(nombre_parcial)
        return str(result)

    @kernel_function(
        description="Obtener eventos por línea de transmisión usando su ID"
    )
    @kernel_function_context_parameter(name="id_linea", description="ID de la línea de transmisión")
    def obtener_eventos_por_linea(self, id_linea: str) -> str:
        try:
            result = self.plugin.obtener_eventos_por_linea(int(id_linea))
            return str(result)
        except ValueError:
            return "El valor de 'id_linea' debe ser un número entero"

    @kernel_function(
        description="Ejecutar una consulta SQL libre. Solo se permiten SELECT por seguridad."
    )
    @kernel_function_context_parameter(name="query", description="Consulta SQL completa (solo SELECT)")
    def consulta_sql_libre(self, query: str) -> str:
        result = self.plugin.consulta_sql_libre(query)
        return str(result)
