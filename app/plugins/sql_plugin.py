import psycopg2
import os


class SqlPlugin:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
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

    # 🔌 Fallas por comuna
    def obtener_fallas_por_comuna_con_fallback(self, comuna: str):
        comuna = comuna.strip().lower()
        query_eventos = """
            SELECT c.id, c.tipo_evento, c.fecha_evento,
                   ST_AsGeoJSON(c.ubicacion) AS geojson,
                   e.nombre_comuna
            FROM comunas_chile e
            JOIN eventos_transmision c ON ST_Intersects(ST_Transform(c.ubicacion, 3857), e.geom)
            WHERE LOWER(e.nombre_comuna) = %s
              AND c.fecha_evento >= CURRENT_DATE - INTERVAL '7 days'
        """
        eventos = self._run_query(query_eventos, (comuna,))
        if eventos:
            return eventos

        fallback = """
            SELECT e.nombre_comuna, COUNT(*) as cantidad_fallas
            FROM comunas_chile e
            JOIN eventos_transmision c ON ST_Intersects(ST_Transform(c.ubicacion, 3857), e.geom)
            WHERE c.fecha_evento >= CURRENT_DATE - INTERVAL '7 days'
            GROUP BY e.nombre_comuna
            ORDER BY cantidad_fallas DESC
            LIMIT 10
        """
        resumen = self._run_query(fallback)
        return [{
            "mensaje": f"No se encontraron fallas en la comuna '{comuna}'.",
            "sugerencia": "Aquí tienes comunas con fallas recientes.",
            "resumen": resumen
        }]

    # 📡 Líneas y comunas
    def obtener_lineas_transmision(self):
        return self._run_query("SELECT id, nombre, codigo, voltaje FROM lineas_transmision")

    def obtener_comunas(self):
        return self._run_query("SELECT nombre_comuna FROM comunas_chile ORDER BY nombre_comuna")

    # Calles
    def obtener_calles(self, nombre_parcial: str):
        query = """
            SELECT name, ST_AsText(ST_Centroid(geometry)) AS centroide
            FROM way
            WHERE name ILIKE %s
            LIMIT 20
        """
        return self._run_query(query, (f"%{nombre_parcial}%",))

    # Eventos por línea
    def obtener_eventos_por_linea(self, id_linea: int):
        query = """
            SELECT id, tipo_evento, fecha_evento, ST_AsGeoJSON(ubicacion) AS geojson
            FROM eventos_transmision
            WHERE linea_id = %s
              AND fecha_evento >= CURRENT_DATE - INTERVAL '30 days'
        """
        return self._run_query(query, (id_linea,))

    # SQL libre (solo SELECT)
    def consulta_sql_libre(self, query: str):
        if not query.strip().lower().startswith("select"):
            return [{"error": "Solo se permiten consultas SELECT por seguridad."}]
        return self._run_query(query)

    # Criticidad
    def obtener_eventos_con_criticidad(self, comuna: str):
        query = """
            SELECT c.id, c.tipo_evento, c.fecha_evento, c.criticidad,
                   ST_AsGeoJSON(c.ubicacion) AS geojson, e.nombre_comuna
            FROM comunas_chile e
            JOIN eventos_transmision c ON ST_Intersects(ST_Transform(c.ubicacion, 3857), e.geom)
            WHERE LOWER(e.nombre_comuna) = %s
              AND c.fecha_evento >= CURRENT_DATE - INTERVAL '30 days'
        """
        return self._run_query(query, (comuna,))

    # Clima
    def obtener_clima_actual_por_comuna(self, comuna: str):
        query = """
            SELECT fecha, lluvia_mm, viento_kmh, temperatura, riesgo_climatico
            FROM clima_por_comuna
            WHERE LOWER(comuna) = %s
            ORDER BY fecha DESC
            LIMIT 1
        """
        return self._run_query(query, (comuna,))

    # Riesgo zonal
    def obtener_riesgos_zonales_por_comuna(self, comuna: str):
        query = """
            SELECT r.zona, r.tipo_riesgo, r.nivel
            FROM riesgo_zonal r
            JOIN comunas_chile c ON ST_Intersects(r.geom, c.geom)
            WHERE LOWER(c.nombre_comuna) = %s
        """
        return self._run_query(query, (comuna,))

    # Geocodificación local
    def geocodificar_direccion_local(self, calle: str, comuna: str):
        query = """
            SELECT ST_X(ST_Centroid(w.geometry)) AS lon,
                   ST_Y(ST_Centroid(w.geometry)) AS lat
            FROM way w
            JOIN comunas_chile c ON ST_Intersects(w.geometry, c.geom)
            WHERE LOWER(w.name) ILIKE LOWER(%s)
              AND LOWER(c.nombre_comuna) = LOWER(%s)
              AND w.geometry IS NOT NULL
            LIMIT 1
        """
        return self._run_query(query, (calle, comuna))

    # Crear evento
    def crear_evento_cercano(self, lat: float, lon: float, tipo_evento: str, criticidad: str):
        query = """
            WITH linea_cercana AS (
                SELECT id
                FROM lineas_transmision
                ORDER BY geom <-> ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), 4326), 3857)
                LIMIT 1
            )
            INSERT INTO eventos_transmision (
                tipo_evento,
                fecha_evento,
                ubicacion,
                criticidad,
                linea_id
            ) VALUES (
                %s,
                CURRENT_TIMESTAMP,
                ST_SetSRID(ST_MakePoint(%s, %s), 4326),
                %s,
                (SELECT id FROM linea_cercana)
            )
            RETURNING id;
        """
        return self._run_query(query, (lon, lat, tipo_evento, lon, lat, criticidad))

    # Brigada más cercana
    def obtener_brigada_mas_cercana(self, lat: float, lon: float):
        query = """
            SELECT id, numero_brigada, nombre_comuna,
                   ST_AsGeoJSON(ubicacion) AS geojson,
                   ST_Distance(ubicacion, ST_SetSRID(ST_MakePoint(%s, %s), 4326)) AS distancia
            FROM brigadas_por_comuna
            ORDER BY ubicacion <-> ST_SetSRID(ST_MakePoint(%s, %s), 4326)
            LIMIT 1
        """
        return self._run_query(query, (lon, lat, lon, lat))

    # Evento más cercano a coordenadas
    def obtener_evento_mas_cercano_a_punto(self, lat: float, lon: float):
        query = """
            SELECT id, tipo_evento, fecha_evento,
                   ST_AsGeoJSON(ubicacion) AS geojson,
                   ST_Distance(ubicacion, ST_SetSRID(ST_MakePoint(%s, %s), 4326)) AS distancia
            FROM eventos_transmision
            ORDER BY ubicacion <-> ST_SetSRID(ST_MakePoint(%s, %s), 4326)
            LIMIT 1
        """
        return self._run_query(query, (lon, lat, lon, lat))
