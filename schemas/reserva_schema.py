
from pydantic import BaseModel
from typing import Optional

class ReservaSchema(BaseModel):
    id_usuario = int
    id_horario = int
    
