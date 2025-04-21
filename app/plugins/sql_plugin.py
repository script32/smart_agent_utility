import os
import psycopg2
from dotenv import load_dotenv
from typing import List

load_dotenv()

class SqlPlugin:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT", 5432),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )

    def _run_query(self, query: str, params: tuple = ()) -> list:
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                if cur.description:
                    columns = [desc[0] for desc in cur.description]
                    rows = cur.fetchall()
                    return [dict(zip(columns, row)) for row in rows]
                else:
                    self.conn.commit()
                    return [{"status": "ok"}]
        except Exception as e:
            return [{"error": str(e)}]


    def obtener_fallas_por_comuna_con_fallback(self, comuna: str):
        comuna = comuna.strip().lower()

        # Consulta principal con cruce geográfico
        query_eventos = """
            SELECT c.id, c.tipo_evento, c.fecha_evento,
                ST_AsGeoJSON(c.ubicacion) AS geojson,
                e.nombre_comuna
            FROM comunas_chile e
            JOIN eventos_transmision c
            ON ST_Intersects(ST_Transform(c.ubicacion, 3857), e.geom)
            WHERE LOWER(e.nombre_comuna) = %s
            AND c.fecha_evento >= CURRENT_DATE - INTERVAL '7 days'
        """
        eventos = self._run_query(query_eventos, (comuna,))

        if eventos:
            return eventos

        # Si no se encuentra la comuna, devolver resumen de otras comunas con fallas
        fallback_query = """
            SELECT e.nombre_comuna, COUNT(*) as cantidad_fallas
            FROM comunas_chile e
            JOIN eventos_transmision c
            ON ST_Intersects(ST_Transform(c.ubicacion, 3857), e.geom)
            WHERE c.fecha_evento >= CURRENT_DATE - INTERVAL '7 days'
            GROUP BY e.nombre_comuna
            ORDER BY cantidad_fallas DESC
        """
        resumen = self._run_query(fallback_query)

        return [{
            "mensaje": f"No se encontraron fallas en la comuna '{comuna}'.",
            "sugerencia": "Aquí tienes una lista de comunas con fallas recientes. Si quieres más detalles, indícame una de ellas.",
            "resumen": resumen
        }]


    def obtener_lineas_transmision(self):
        return self._run_query("SELECT id, nombre, ST_AsGeoJSON(geom) as geojson FROM lineas_transmision")

    def obtener_comunas(self):
        return self._run_query("SELECT nombre, ST_AsGeoJSON(geom) as geojson FROM comunas")

    def obtener_calles(self, nombre_parcial: str):
        return self._run_query(f"""
            SELECT nombre, ST_AsGeoJSON(geom) as geojson 
            FROM calles 
            WHERE LOWER(nombre) LIKE LOWER('%{nombre_parcial}%')
        """)

    def obtener_eventos_por_linea(self, id_linea: int):
        return self._run_query(f"""
            SELECT e.*, l.nombre 
            FROM eventos e
            JOIN lineas_transmision l ON ST_Intersects(e.geom, l.geom)
            WHERE l.id = {id_linea}
        """)

    # Función general para consultas libres seguras
    def consulta_sql_libre(self, query: str):
        query = query.strip().lower()
        if not query.startswith("select"):
            return [{"error": "Solo se permiten consultas SELECT"}]
        return self._run_query(query)
