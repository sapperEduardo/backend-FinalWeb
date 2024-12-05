from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.user_rutes import user_router
from routers.horario_rutes import horario_router
from routers.reserva_rutes import reserva_router

app = FastAPI()

# Lista de orígenes permitidos. Añade más dominios si es necesario.
origins = [
    "http://127.0.0.1:5500",   # Desarrollo local
    "http://localhost:5500",   # Alternativa localhost
    "https://gymfitgym.netlify.app",  # Dominio de tu aplicación frontend en producción
    "https://backend-finalweb.onrender.com"  # Dominio del backend en producción
]

# Configuración del middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir los orígenes especificados
    allow_credentials=True,  # Permitir el uso de cookies
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Métodos específicos
    allow_headers=["Content-Type", "Authorization"],  # Encabezados específicos
)

@app.get("/")
def get():
    return {"Estado": "Correcto!"}

# Registrar los routers
app.include_router(user_router)
app.include_router(horario_router)
app.include_router(reserva_router)
