
from pydantic import BaseModel
from typing import Optional

class HorarioSchema(BaseModel):
    id: Optional[int]
    nombre: str
    descripcion: str
    horario: str
    cupos: int
    
