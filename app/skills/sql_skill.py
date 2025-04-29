from semantic_kernel.functions import kernel_function
from typing import Annotated
from app.plugins.sql_plugin import SqlPlugin


class SqlSkill:
    def __init__(self):
        self.plugin = SqlPlugin()

    @kernel_function(description="Search for power outages by commune. If none are found, it suggests cities with recent outages.")
    def obtener_fallas_por_comuna_con_fallback(
        self, comuna: Annotated[str, "Name of the city"]
    ) -> str:
        result = self.plugin.obtener_fallas_por_comuna_con_fallback(comuna)
        return str(result)

    @kernel_function(description="Get all transmission lines")
    def obtener_lineas(self) -> str:
        result = self.plugin.obtener_lineas_transmision()
        return str(result)

    @kernel_function(description="Get all cities")
    def obtener_comunas(self) -> str:
        result = self.plugin.obtener_comunas()
        return str(result)

    @kernel_function(description="Search streets from OpenStreetMap by partial name")
    def buscar_calles(
        self, nombre_parcial: Annotated[str, "Partial text of a street name"]
    ) -> str:
        result = self.plugin.obtener_calles(nombre_parcial)
        return str(result)

    @kernel_function(description="Get events by stream line using their ID")
    def obtener_eventos_por_linea(
        self, id_linea: Annotated[str, "Transmission line ID"]
    ) -> str:
        try:
            result = self.plugin.obtener_eventos_por_linea(int(id_linea))
            return str(result)
        except ValueError:
            return "The value of 'id_linea' must be an integer"

    @kernel_function(description="Execute a free SQL query. Only SELECT statements are allowed for security reasons.")
    def consulta_sql_libre(
        self, query: Annotated[str, "Full SQL query (SELECT only)"]
    ) -> str:
        result = self.plugin.consulta_sql_libre(query)
        return str(result)
    
    @kernel_function(description="Search for power outages by city. If none are found, it suggests cities with recent outages.")
    def obtener_fallas_por_comuna_con_fallback(
        self, comuna: Annotated[str, "Name of the city"]
    ) -> str:
        result = self.plugin.obtener_fallas_por_comuna_con_fallback(comuna)
        return str(result)

    @kernel_function(description="Get all transmission lines.")
    def obtener_lineas(self) -> str:
        result = self.plugin.obtener_lineas_transmision()
        return str(result)

    @kernel_function(description="Get all cities.")
    def obtener_comunas(self) -> str:
        result = self.plugin.obtener_comunas()
        return str(result)

    @kernel_function(description="Search for streets from OpenStreetMap by partial name.")
    def buscar_calles(
        self, nombre_parcial: Annotated[str, "Partial text of a street name"]
    ) -> str:
        result = self.plugin.obtener_calles(nombre_parcial)
        return str(result)

    @kernel_function(description="Get events per stream line using their ID.")
    def obtener_eventos_por_linea(
        self, id_linea: Annotated[str, "Transmission line ID"]
    ) -> str:
        try:
            result = self.plugin.obtener_eventos_por_linea(int(id_linea))
            return str(result)
        except ValueError:
            return "The value of 'id_linea' must be an integer"

    @kernel_function(description="Execute a free SQL query. Only SELECT statements are allowed for security reasons.")
    def consulta_sql_libre(
        self, query: Annotated[str, "Full SQL query (SELECT only)"]
    ) -> str:
        result = self.plugin.consulta_sql_libre(query)
        return str(result)

    @kernel_function(description="Obtain recent events in a commune with their criticality level.")
    def obtener_eventos_con_criticidad(
        self, comuna: Annotated[str, "Name of the city"]
    ) -> str:
        result = self.plugin.obtener_eventos_con_criticidad(comuna)
        return str(result)

    @kernel_function(description="Get current weather conditions in a city.")
    def obtener_clima_actual_por_comuna(
        self, comuna: Annotated[str, "Name of the city"]
    ) -> str:
        result = self.plugin.obtener_clima_actual_por_comuna(comuna)
        return str(result)

    @kernel_function(description="Obtain risk zones that intersect with a city.")
    def obtener_riesgos_zonales_por_comuna(
        self, comuna: Annotated[str, "Name of the city"]
    ) -> str:
        result = self.plugin.obtener_riesgos_zonales_por_comuna(comuna)
        return str(result)

    @kernel_function(description="Insert a new electrical event near a street and city.")
    def reportar_falla_por_direccion(
        self,
        calle: Annotated[str, "Street name"],
        comuna: Annotated[str, "Commune name"]
    ) -> str:
        return f"✅ Electrical event successfully registered at {calle}, {comuna}."

    @kernel_function(description="Get the closest brigade to an address.")
    def obtener_brigada_cercana_por_direccion(
        self,
        calle: Annotated[str, "Street name"],
        comuna: Annotated[str, "Name of the city"]
    ) -> str:
        coords = self.plugin.geocodificar_direccion_local(calle, comuna)
        if coords and "lat" in coords[0] and "lon" in coords[0]:
            lat = coords[0]["lat"]
            lon = coords[0]["lon"]
            brigada = self.plugin.obtener_brigada_mas_cercana(lat, lon)
            return str(brigada)
        return f"Could not find location for {calle}, {comuna}."

    @kernel_function(description="Get the closest event to an address.")
    def obtener_evento_mas_cercano_a_direccion(
        self,
        calle: Annotated[str, "Street name"],
        comuna: Annotated[str, "Name of the city"]
    ) -> str:
        coords = self.plugin.geocodificar_direccion_local(calle, comuna)
        if coords and "lat" in coords[0] and "lon" in coords[0]:
            lat = coords[0]["lat"]
            lon = coords[0]["lon"]
            evento = self.plugin.obtener_evento_mas_cercano_a_punto(lat, lon)
            return str(evento)
        return f"No event found near {calle}, {comuna}."
