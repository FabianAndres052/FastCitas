from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Usuario
from pydantic import BaseModel

router = APIRouter()

class RegisterSchema(BaseModel):
    nombre: str
    email: str
    password: str
    rol: str = "paciente"

class LoginSchema(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    existe = db.query(Usuario).filter(Usuario.email == data.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    usuario = Usuario(nombre=data.nombre, email=data.email, password=data.password, rol=data.rol)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return {"mensaje": "Usuario registrado", "usuario": {"id": usuario.id, "nombre": usuario.nombre, "rol": usuario.rol}}

@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == data.email, Usuario.password == data.password).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {"mensaje": "Login exitoso", "usuario": {"id": usuario.id, "nombre": usuario.nombre, "rol": usuario.rol}}