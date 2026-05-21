from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import autenticacion, citas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastCitas API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(autenticacion.router, prefix="/auth", tags=["Auth"])
app.include_router(citas.router, prefix="/citas", tags=["Citas"])

@app.get("/")
def root():
    return {"mensaje": "FastCitas API corriendo"}