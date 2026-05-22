from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
import models
import secrets
from datetime import datetime, timedelta

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
    fecha_nacimiento: str = ""

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
        "fecha_nacimiento": usuario.fecha_nacimiento or "",
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
        rol=data.rol,
        fecha_nacimiento=data.fecha_nacimiento
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
            foto_iniciales=iniciales,
            activo=0
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

# Solicitar restablecimiento de contraseña
@router.post("/solicitar-reset")
def solicitar_reset(email: str, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Correo no encontrado")
    # Generar token seguro
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(hours=1)
    reset = models.PasswordResetToken(usuario_id=usuario.id, token=token, expires_at=expires_at)
    db.add(reset)
    db.commit()
    # Enviar correo (simulado aquí; integración con envío real de email)
    # Aquí simplemente devolvemos el token para pruebas
    return {"mensaje": "Solicitud enviada", "token": token}

# Validar token
@router.get("/validar-token")
def validar_token(token: str, db: Session = Depends(get_db)):
    reset = db.query(models.PasswordResetToken).filter(models.PasswordResetToken.token == token).first()
    if not reset or reset.expires_at < datetime.utcnow() or reset.used:
        raise HTTPException(status_code=400, detail="Token inválido o expirado")
    return {"valido": True}

# Restablecer contraseña usando token
@router.put("/reset-password")
def reset_password(token: str, nueva_password: str, db: Session = Depends(get_db)):
    reset = db.query(models.PasswordResetToken).filter(models.PasswordResetToken.token == token).first()
    if not reset or reset.expires_at < datetime.utcnow() or reset.used:
        raise HTTPException(status_code=400, detail="Token inválido o expirado")
    usuario = db.query(models.Usuario).filter(models.Usuario.id == reset.usuario_id).first()
    usuario.password = nueva_password
    reset.used = 1
    db.commit()
    return {"mensaje": "Contraseña restablecida correctamente"}

@router.get("/verificar-email")
def verificar_email(email: str, db: Session = Depends(get_db)):
    existe = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    if not existe:
        raise HTTPException(status_code=404, detail="No existe una cuenta con ese correo")
    return {"existe": True}

@router.get("/usuarios")
def obtener_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(models.Usuario).all()
    return [{"id": u.id, "nombre": u.nombre, "email": u.email, "rol": u.rol} for u in usuarios]