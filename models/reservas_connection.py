import psycopg
from config import db


class ReservaConnection():
    conn = None
    def __init__(self):
        try:
            self.conn = psycopg.connect(f"dbname={db.DB} user={db.USER} password={db.PASSWORD} host={db.HOST} port={db.PORT}")
            print("Conectado con exito!")
        except psycopg.OperationalError as err:
            print("Error al conectarse!")
            print(err)
            self.conn.close()


    def reservar_clase(self, id_usuario, id_horario):
        with self.conn.cursor() as cur:
            cur.execute("""
        INSERT INTO "reservas"(
            idusuario, idhorario)
            VALUES (%s, %s);
        """, (id_usuario,id_horario))
        self.conn.commit()


    def cancelar_reserva(self, id_usuario, id_horario):
        with self.conn.cursor() as cur:
            cur.execute("""
        DELETE FROM "reservas"
            WHERE idusuario = %s and idhorario = %s;
        """, (id_usuario,id_horario))
        self.conn.commit()


    def read_all(self):
        with self.conn.cursor() as cur:
            data = cur.execute("""
        SELECT * FROM "reservas";
        """)
            return data.fetchall()


    def read_one(self, id_usuario, id_horario):
        with self.conn.cursor() as cur:
            data = cur.execute("""
        SELECT * FROM "reservas" WHERE idusuario = %s and idhorario = %s;
        """, (id_usuario,id_horario))
            
            return {"reserva": bool(data)}




    def __def__(self):
        self.conn.close()



