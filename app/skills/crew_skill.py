from semantic_kernel.functions import kernel_function
from typing import Annotated
from app.plugins.sql_plugin import SqlPlugin

class CrewSkill:
    def __init__(self):
        self.plugin = SqlPlugin()

    @kernel_function(description="Obtener cuadrillas disponibles en una comuna.")
    def obtener_cuadrillas_por_comuna(
        self, comuna: Annotated[str, "Nombre de la comuna"]
    ) -> str:
        query = """
            SELECT id, numero_brigada, nombre_comuna, ST_AsGeoJSON(ubicacion) AS geojson
            FROM brigadas_por_comuna
            WHERE LOWER(nombre_comuna) = LOWER(%s)
        """
        result = self.plugin._run_query(query, (comuna,))
        return str(result)

    @kernel_function(description="Buscar la brigada más cercana a una dirección.")
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

    @kernel_function(description="Asignar brigada más cercana a un evento por dirección.")
    def asignar_brigada_a_direccion(
        self,
        calle: Annotated[str, "Nombre de la calle donde ocurrió el evento"],
        comuna: Annotated[str, "Nombre de la comuna donde ocurrió el evento"]
    ) -> str:
        coords = self.plugin.geocodificar_direccion_local(calle, comuna)
        if not coords or "lat" not in coords[0] or "lon" not in coords[0]:
            return f"No se pudo geolocalizar la dirección '{calle}' en la comuna '{comuna}'."

        lat = coords[0]["lat"]
        lon = coords[0]["lon"]

        # Buscar evento más cercano
        evento = self.plugin.obtener_evento_mas_cercano_a_punto(lat, lon)
        if not evento or "id" not in evento[0]:
            return f"No se encontró un evento cercano a esa ubicación."

        evento_id = evento[0]["id"]

        # Buscar brigada más cercana
        brigada = self.plugin.obtener_brigada_mas_cercana(lat, lon)
        if not brigada or "id" not in brigada[0]:
            return f"No se encontró ninguna brigada disponible en la zona."

        brigada_id = brigada[0]["id"]

        # Insertar asignación
        insert_query = """
            INSERT INTO asignaciones_eventos (evento_id, brigada_id)
            VALUES (%s, %s)
            RETURNING id
        """
        asignacion = self.plugin._run_query(insert_query, (evento_id, brigada_id))
        return f"Brigada asignada al evento más cercano. ID asignación: {asignacion[0]['id']}"
