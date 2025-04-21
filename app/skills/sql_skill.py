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
    
    @kernel_function(description="Buscar fallas eléctricas por comuna. Si no encuentra, sugiere comunas con fallas recientes.")
    def obtener_fallas_por_comuna_con_fallback(
        self, comuna: Annotated[str, "Nombre de la comuna"]
    ) -> str:
        result = self.plugin.obtener_fallas_por_comuna_con_fallback(comuna)
        return str(result)

    @kernel_function(description="Obtener todas las líneas de transmisión.")
    def obtener_lineas(self) -> str:
        result = self.plugin.obtener_lineas_transmision()
        return str(result)

    @kernel_function(description="Obtener todas las comunas.")
    def obtener_comunas(self) -> str:
        result = self.plugin.obtener_comunas()
        return str(result)

    @kernel_function(description="Buscar calles desde OpenStreetMap por nombre parcial.")
    def buscar_calles(
        self, nombre_parcial: Annotated[str, "Texto parcial del nombre de una calle"]
    ) -> str:
        result = self.plugin.obtener_calles(nombre_parcial)
        return str(result)

    @kernel_function(description="Obtener eventos por línea de transmisión usando su ID.")
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

    # 🟩 FUNCIONES NUEVAS

    @kernel_function(description="Obtener eventos recientes en una comuna con su nivel de criticidad.")
    def obtener_eventos_con_criticidad(
        self, comuna: Annotated[str, "Nombre de la comuna"]
    ) -> str:
        result = self.plugin.obtener_eventos_con_criticidad(comuna)
        return str(result)

    @kernel_function(description="Obtener condiciones climáticas actuales en una comuna.")
    def obtener_clima_actual_por_comuna(
        self, comuna: Annotated[str, "Nombre de la comuna"]
    ) -> str:
        result = self.plugin.obtener_clima_actual_por_comuna(comuna)
        return str(result)

    @kernel_function(description="Obtener zonas de riesgo que intersectan con una comuna.")
    def obtener_riesgos_zonales_por_comuna(
        self, comuna: Annotated[str, "Nombre de la comuna"]
    ) -> str:
        result = self.plugin.obtener_riesgos_zonales_por_comuna(comuna)
        return str(result)

    @kernel_function(description="Insertar un nuevo evento eléctrico cerca de una calle y comuna.")
    def reportar_falla_por_direccion(
        self,
        calle: Annotated[str, "Nombre de la calle o avenida"],
        comuna: Annotated[str, "Nombre de la comuna donde está la dirección"]
    ) -> str:
        coords = self.plugin.geocodificar_direccion_local(calle, comuna)
        if coords and "lat" in coords[0] and "lon" in coords[0]:
            lat = coords[0]["lat"]
            lon = coords[0]["lon"]
            resultado = self.plugin.crear_evento_cercano(lat, lon, "Reporte ciudadano", "media")
            return f"Falla reportada cerca de {calle}, {comuna}. ID del evento: {resultado[0]['id']}"
        return f"No se pudo geolocalizar la dirección '{calle}' en la comuna '{comuna}'."

    @kernel_function(description="Obtener la brigada más cercana a una dirección.")
    def obtener_brigada_cercana_por_direccion(
        self,
        calle: Annotated[str, "Nombre de la calle"],
        comuna: Annotated[str, "Nombre de la comuna"]
    ) -> str:
        coords = self.plugin.geocodificar_direccion_local(calle, comuna)
        if coords and "lat" in coords[0] and "lon" in coords[0]:
            lat = coords[0]["lat"]
            lon = coords[0]["lon"]
            brigada = self.plugin.obtener_brigada_mas_cercana(lat, lon)
            return str(brigada)
        return f"No se pudo encontrar la ubicación para {calle}, {comuna}."

    @kernel_function(description="Obtener el evento más cercano a una dirección.")
    def obtener_evento_mas_cercano_a_direccion(
        self,
        calle: Annotated[str, "Nombre de la calle"],
        comuna: Annotated[str, "Nombre de la comuna"]
    ) -> str:
        coords = self.plugin.geocodificar_direccion_local(calle, comuna)
        if coords and "lat" in coords[0] and "lon" in coords[0]:
            lat = coords[0]["lat"]
            lon = coords[0]["lon"]
            evento = self.plugin.obtener_evento_mas_cercano_a_punto(lat, lon)
            return str(evento)
        return f"No se encontró ningún evento cercano a {calle}, {comuna}."
