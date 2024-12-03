
from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: Optional[int]
    nombre: str
    correo: str
    telefono: str
    contraseña: str
    
