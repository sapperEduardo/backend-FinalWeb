import psycopg
from config import db
from schemas.user_schema import UserSchema

class UserConnection():
    conn = None
    def __init__(self):
        try:
            self.conn = psycopg.connect(f"dbname={db.DB} user={db.USER} password={db.PASSWORD} host={db.HOST} port={db.PORT}")
            print("Conectado con exito!")
        except psycopg.OperationalError as err:
            print("Error al conectarse!")
            print(err)
            self.conn.close()
    


    def write(self, data):
        with self.conn.cursor() as cur:
            cur.execute("""
        INSERT INTO "usuarios"(
	    nombre, correo, telefono, "contraseña")
	VALUES (%(nombre)s, %(correo)s, %(telefono)s, %(contraseña)s); 
        """, data)
        self.conn.commit()

    def read_all(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                SELECT * FROM "usuarios";
                """)
                return cur.fetchall()
        except psycopg.Error as e:
            print(f"Error leyendo todos los usuarios: {e}")
            self.conn.rollback()
            return []



    def read_one(self, id):
        with self.conn.cursor() as cur:
            data = cur.execute("""
        SELECT * FROM "usuarios" WHERE id = %s;
        """, (id,))
            r = data.fetchone()

            if r:
                
                data = UserSchema(id=r[0],
                               nombre=r[1],
                               correo=r[2],
                               telefono=r[3],
                               contraseña=r[4])
                return data
            else:
                return {"estado": "error"}



#### PARA EL LOGIN ###
    def find_user(self, name_or_email, password):
        """
        Busca un usuario por nombre/correo y contraseña.
        
        :param name_or_email: Nombre o correo del usuario.
        :param password: Contraseña del usuario.
        :return: UserSchema en caso de éxito o {"estado": "error"} en caso de fallo.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT id, nombre, correo, telefono, "contraseña"
                FROM "usuarios"
                WHERE (nombre = %(name)s OR correo = %(email)s) AND "contraseña" = %(contraseña)s;
            """, {"name":name_or_email,"email":name_or_email,"contraseña":password})
            
            result = cur.fetchall()

            if result:
                print("exito en inicio de sesion")
                r = result[0]

                data = UserSchema(id=r[0],
                               nombre=r[1],
                               correo=r[2],
                               telefono=r[3],
                               contraseña=r[4])

                return data

            else:

                # Devolver un error si no se encontró un usuario
                print("error de sesion")
                return {"estado": "error"}



    def update_one(self, data):
        with self.conn.cursor() as cur:
            cur.execute("""
        UPDATE "usuarios"
            SET nombre=%(nombre)s, correo=%(correo)s, telefono=%(telefono)s, "contraseña"=%(contraseña)s
            WHERE id=%(id)s;
            """, data)
        self.conn.commit()


    def delete_one(self, id):
        with self.conn.cursor() as cur:
            cur.execute("""
            DELETE FROM "users"	WHERE id = %s;
        """, (id,))
        self.conn.commit()
    





    def __def__(self):
        self.conn.close()



