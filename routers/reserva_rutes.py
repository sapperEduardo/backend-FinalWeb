from fastapi import APIRouter

from models.reservas_connection import ReservaConnection
from models.horario_connection import HorarioConnection
from schemas.horario_schema import HorarioSchema

reserva_router = APIRouter()

reservaConn = ReservaConnection()
horaConn = HorarioConnection()


@reserva_router.get("/reservas")
def get_all_reservas():
    data = reservaConn.read_all()
    
    return [{"id_usuario": u, "id_horario": h} for u,h in data]


@reserva_router.post("/reservar/{id_usuario}/{id_horario}")
def reservar_clase(id_usuario:str, id_horario:str):
    reservaConn.reservar_clase(id_usuario,id_horario)

    horaConn.disminuir_cupo(id_horario, 1)

    return {"ESTADO":"CORRECTO"}    


@reserva_router.delete("/cancelar/{id_usuario}/{id_horario}")
def reservar_clase(id_usuario, id_horario):
    reservaConn.cancelar_reserva(id_usuario,id_horario)

    horaConn.aumentar_cupo(id_horario, 1)

    return {"ESTADO":"CORRECTO"}    




