from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.user_rutes import user_router
from routers.horario_rutes import horario_router
from routers.reserva_rutes import reserva_router

app = FastAPI()


origins = [
    "http://127.0.0.1:5500",  # Permite tu origen de desarrollo
    "http://localhost:5500",  # Alternativa por si usas localhost
    # Añade otros orígenes si los necesitas
]

# Configura el middleware CORS
app.add_middleware(
    CORSMiddleware,
allow_origins=["https://gymfitgym.netlify.app", "http://localhost:5173"]            # Permitir los orígenes especificados
    allow_credentials=True,            # Permitir el uso de cookies
    allow_methods=["*"],               # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],               # Permitir todos los encabezados
)


@app.get("/")
def get():
    return {"Estado":"Correcto!"}


app.include_router(user_router)
app.include_router(horario_router)
app.include_router(reserva_router)

