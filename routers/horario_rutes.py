from fastapi import APIRouter

from models.horario_connection import HorarioConnection
from schemas.horario_schema import HorarioSchema

horario_router = APIRouter()

horaConn = HorarioConnection()





@horario_router.get("/horarios")
def get_horarios():
    dias_validos = [
        "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"
    ]
    calendario = {}
    for dia in dias_validos:
        horarios = horaConn.get_horarios_por_dia(dia)
        calendario[dia] = horarios
    return calendario


@horario_router.get("/horarios/disponibles/{id}")
def get_horarios_disponibles(id: int):
    dias_validos = [
        "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"
    ]
    calendario = {}
    for dia in dias_validos:
        horarios = []
        if id:
            horarios = horaConn.get_horarios_disopnibles_usuario(dia, id)
        calendario[dia] = horarios
    return calendario


@horario_router.get("/horarios/reservados/{id}")
def get_horarios_disponibles(id: int):
    dias_validos = [
        "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"
    ]
    calendario = {}
    for dia in dias_validos:
        horarios = []
        if id:
            horarios = horaConn.get_horarios_reservados_usuario(dia, id)
        calendario[dia] = horarios
    return calendario










