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

    def _run_query(self, query: str) -> List[dict]:
        try:
            with self.conn.cursor() as cur:
                cur.execute(query)
                if cur.description:
                    columns = [desc[0] for desc in cur.description]
                    rows = cur.fetchall()
                    return [dict(zip(columns, row)) for row in rows]
                else:
                    self.conn.commit()
                    return [{"status": "ok"}]
        except Exception as e:
            return [{"error": str(e)}]

    # Consultas específicas por tabla
    def obtener_fallas_recientes(self, comuna: str):
        return self._run_query(f"""
            SELECT * FROM eventos 
            WHERE comuna = '{comuna}' 
              AND fecha >= current_date - interval '7 days'
        """)

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
