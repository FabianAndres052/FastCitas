from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
import models

router = APIRouter()

class LoginData(BaseModel):
    email: str
    password: str

class RegistroData(BaseModel):
    nombre: str
    email: str
    password: str
    rol: str = "paciente"
    especialidad: str = ""
    telefono: str = ""

class CambiarPasswordData(BaseModel):
    email: str
    nueva_password: str

@router.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == data.email,
        models.Usuario.password == data.password
    ).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    extra = {}
    if usuario.rol == "doctor":
        doctor = db.query(models.Doctor).filter(models.Doctor.usuario_id == usuario.id).first()
        if doctor:
            extra = {"doctor_id": doctor.id, "especialidad": doctor.especialidad}
    
    return {"usuario": {
        "id": usuario.id,
        "nombre": usuario.nombre,
        "email": usuario.email,
        "rol": usuario.rol,
        **extra
    }}

@router.post("/register")
def register(data: RegistroData, db: Session = Depends(get_db)):
    existe = db.query(models.Usuario).filter(models.Usuario.email == data.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    if data.rol == "admin":
        raise HTTPException(status_code=403, detail="No se puede registrar como administrador")
    
    nuevo = models.Usuario(
        nombre=data.nombre,
        email=data.email,
        password=data.password,
        rol=data.rol
    )
    db.add(nuevo)
    db.flush()

    if data.rol == "doctor":
        iniciales = "".join([p[0].upper() for p in data.nombre.replace("Dr. ", "").replace("Dra. ", "").split()[:2]])
        db.add(models.Doctor(
            nombre=data.nombre,
            especialidad=data.especialidad,
            email=data.email,
            telefono=data.telefono,
            usuario_id=nuevo.id,
            foto_iniciales=iniciales
        ))

    db.commit()
    return {"mensaje": "Usuario registrado correctamente"}

@router.put("/cambiar-password")
def cambiar_password(data: CambiarPasswordData, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == data.email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="No existe una cuenta con ese correo")
    usuario.password = data.nueva_password
    db.commit()
    return {"mensaje": "Contraseña actualizada correctamente"}

@router.get("/usuarios")
def obtener_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(models.Usuario).all()
    return [{"id": u.id, "nombre": u.nombre, "email": u.email, "rol": u.rol} for u in usuarios]