from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal, Base
from routes import autenticacion, citas, doctores
from sqlalchemy import text
import models

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
app.include_router(doctores.router, prefix="/doctores", tags=["Doctores"])

@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    try:
        # Dynamic migration to add fecha_nacimiento if missing
        columnas = db.execute(text("SHOW COLUMNS FROM usuarios LIKE 'fecha_nacimiento'")).fetchall()
        if not columnas:
            db.execute(text("ALTER TABLE usuarios ADD COLUMN fecha_nacimiento VARCHAR(50) NULL"))
            db.commit()

        # Dynamic migration to add activo if missing to doctores
        columnas_doc = db.execute(text("SHOW COLUMNS FROM doctores LIKE 'activo'")).fetchall()
        if not columnas_doc:
            db.execute(text("ALTER TABLE doctores ADD COLUMN activo INTEGER DEFAULT 0"))
            db.commit()
            db.execute(text("UPDATE doctores SET activo = 1"))
            db.commit()

        # Admin por defecto
        admin = db.query(models.Usuario).filter(models.Usuario.email == "admin@fastcitas.com").first()
        if not admin:
            db.add(models.Usuario(
                nombre="Administrador",
                email="admin@fastcitas.com",
                password="admin123",
                rol="admin",
                fecha_nacimiento="1990-01-01"
            ))
            db.commit()

        # Doctores por defecto
        doctores_default = [
            {"nombre": "Dr. Carlos Mendoza", "especialidad": "Medicina General", "email": "carlos.mendoza@fastcitas.com", "telefono": "3001234567"},
            {"nombre": "Dra. Laura Gómez",   "especialidad": "Pediatría",        "email": "laura.gomez@fastcitas.com",   "telefono": "3019876543"},
            {"nombre": "Dr. Andrés Ruiz",    "especialidad": "Cardiología",      "email": "andres.ruiz@fastcitas.com",   "telefono": "3025551234"},
            {"nombre": "Dra. Sofía Torres",  "especialidad": "Dermatología",     "email": "sofia.torres@fastcitas.com",  "telefono": "3034567890"},
            {"nombre": "Dr. Miguel Vargas",  "especialidad": "Neurología",       "email": "miguel.vargas@fastcitas.com", "telefono": "3041112233"},
        ]

        for d in doctores_default:
            existe = db.query(models.Doctor).filter(models.Doctor.email == d["email"]).first()
            if not existe:
                # Crear usuario para el doctor
                usuario_doc = db.query(models.Usuario).filter(models.Usuario.email == d["email"]).first()
                if not usuario_doc:
                    usuario_doc = models.Usuario(
                        nombre=d["nombre"],
                        email=d["email"],
                        password="doctor123",
                        rol="doctor"
                    )
                    db.add(usuario_doc)
                    db.flush()

                iniciales = "".join([p[0].upper() for p in d["nombre"].replace("Dr. ", "").replace("Dra. ", "").split()[:2]])
                db.add(models.Doctor(
                    nombre=d["nombre"],
                    especialidad=d["especialidad"],
                    email=d["email"],
                    telefono=d["telefono"],
                    usuario_id=usuario_doc.id,
                    foto_iniciales=iniciales,
                    activo=1
                ))
        db.commit()
    finally:
        db.close()

@app.get("/")
def root():
    return {"mensaje": "FastCitas API corriendo"}