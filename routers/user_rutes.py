from fastapi import APIRouter

from models.user_connection import UserConnection
from schemas.user_schema import UserSchema

user_router = APIRouter()

userConn = UserConnection()



@user_router.post("/user")
def post_user(user:UserSchema):
    data = user.dict()
    data.pop("id")
    userConn.write(data)

    return {"ESTADO":"CORRECTO"}    




@user_router.get("/users")
def get_all_users()-> list[UserSchema]:
    data = userConn.read_all()
    
    mapa = [{"id":i,"nombre":n, "correo":p,"telefono":t,"contraseña":c } for i,n,p,t,c in data]

    return mapa

@user_router.get("/user/{id}")
def get_one_user(id:str):
    data = userConn.read_one(id)
    return data

@user_router.delete("/user/{id}")
def delete_one_user(id:str):
    data = userConn.delete_one(id)
    return data



@user_router.get("/user/login/{nombre}/{contrasena}")
def user_login(nombre: str, contrasena: str):
    data = userConn.find_user(nombre, contrasena)

    return data


@user_router.put("/user/{id}")
def update_user(id:str, user:UserSchema):
    data = user.dict()
    data.pop("id")
    data["id"] = id

    userConn.update_one(data)

    return {"ESTADO":"CORRECTO"}    
    










