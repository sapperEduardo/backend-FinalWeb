import psycopg
from config import db
from schemas.horario_schema import HorarioSchema

class HorarioConnection():
    conn = None
    def __init__(self):
        try:
            self.conn = psycopg.connect(f"dbname={db.DB} user={db.USER} password={db.PASSWORD} host={db.HOST} port={db.PORT}")
            print("Conectado con exito!")
        except psycopg.OperationalError as err:
            print("Error al conectarse!")
            print(err)
            self.conn.close()
    
### FUNCION PARA OBTENER A TODOS LOS HORARIOS DE UN DIA
    def get_horarios_por_dia(self, dia: str):
        query = """
            SELECT 
                Horarios.id AS horario_id,
                Clases.nombre AS clase_nombre,
                Clases.descripcion AS clase_descripcion,
                TO_CHAR(Horarios.hora, 'HH24:MI') || ' - ' || 
                TO_CHAR(Horarios.hora + Clases.duracion, 'HH24:MI') AS horario,
                Horarios.cupos AS cupos_disponibles
            FROM 
                Horarios
            INNER JOIN 
                Clases
            ON 
                Horarios.idClase = Clases.id
            WHERE 
                Horarios.dia = %s
                				order by horario;
;
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (dia,))
            rows = cur.fetchall()
        # Transformamos los resultados en una lista de diccionarios
        return [
            {
                "id": row[0],
                "nombre": row[1],
                "descripcion": row[2],
                "horario": row[3],
                "cupos": row[4],
            }
            for row in rows
        ]

### OBTENER HORARIOS DISPONIBLES
    def get_horarios_disopnibles_usuario(self, dia: str, id_usuario):
        query = """
            SELECT 
                Horarios.id AS horario_id,
                Clases.nombre AS clase_nombre,
                Clases.descripcion AS clase_descripcion,
                TO_CHAR(Horarios.hora, 'HH24:MI') || ' - ' || 
                TO_CHAR(Horarios.hora + Clases.duracion, 'HH24:MI') AS horario,
                Horarios.cupos AS cupos_disponibles
            FROM 
                Horarios
            INNER JOIN 
                Clases
                ON Horarios.idClase = Clases.id
            WHERE 
                Horarios.dia = %s
                AND NOT EXISTS (
                    SELECT 1 
                    FROM Reservas 
                    WHERE Reservas.idHorario = Horarios.id 
                    AND Reservas.idUsuario = %s)
                                				order by horario;
;
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (dia, id_usuario))
            rows = cur.fetchall()
        return [
                {
                    "id": row[0],
                    "nombre": row[1],
                    "descripcion": row[2],
                    "horario": row[3],
                    "cupos": row[4],
                }
                for row in rows
            ]


### OBTENER HORARIOS RESERVADOS
    def get_horarios_reservados_usuario(self, dia, id_usuario):
        query = """
            SELECT 
                Horarios.id AS horario_id,
                Clases.nombre AS clase_nombre,
                Clases.descripcion AS clase_descripcion,
                TO_CHAR(Horarios.hora, 'HH24:MI') || ' - ' || 
                TO_CHAR(Horarios.hora + Clases.duracion, 'HH24:MI') AS horario,
                Horarios.cupos AS cupos_disponibles
            FROM 
                Reservas
            INNER JOIN 
                Horarios
                ON Reservas.idHorario = Horarios.id
            INNER JOIN 
                Clases
                ON Horarios.idClase = Clases.id
            WHERE 
                Reservas.idUsuario = %s AND Horarios.dia = %s
                                				order by horario;

                ;
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (id_usuario,dia))
            rows = cur.fetchall()
        return [
            {
                "id": row[0],
                "nombre": row[1],
                "descripcion": row[2],
                "horario": row[3],
                "cupos": row[4],
            }
            for row in rows
        ]


    def write(self, data):
        with self.conn.cursor() as cur:
            cur.execute("""
        INSERT INTO "horarios"(
	    idclase, dia, hora, cupos)
	    VALUES ( %(idClase)s, %(dia)s, %(hora)s, %(cupos)s);
        """, data)
        self.conn.commit()

    def read_all(self):
        with self.conn.cursor() as cur:
            data = cur.execute("""
        SELECT * FROM "horarios";
        """)
            return data.fetchall()


    def read_one(self, id):
        with self.conn.cursor() as cur:
            data = cur.execute("""
        SELECT * FROM "horarios" WHERE id = %s;
        """, (id,))
            
            return data.fetchone()


    def disminuir_cupo(self, id_horario, cant=1):
        query = """
            UPDATE "horarios"
            SET cupos = cupos - %s
            WHERE id = %s;
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (cant, id_horario))
        self.conn.commit()

    def aumentar_cupo(self, id_horario, cant=1):
        query = """
            UPDATE "horarios"
            SET cupos = cupos + %s
            WHERE id = %s;
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (cant, id_horario))
        self.conn.commit()


    def update_one(self, data):
        with self.conn.cursor() as cur:
            cur.execute("""
            UPDATE "horarios" SET idclase= %(idClase)s, dia= %(dia)s, hora=%(hora)s, cupos= %(cupos)s
                        WHERE id= %(id)s
            """, data)
        self.conn.commit()


    def delete_one(self, id):
        with self.conn.cursor() as cur:
            cur.execute("""
            DELETE FROM "horarios"	WHERE id = %s;
        """, (id,))
        self.conn.commit()
    



    def __def__(self):
        self.conn.close()



