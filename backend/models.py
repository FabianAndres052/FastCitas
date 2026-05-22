from sqlalchemy import Column, Integer, String, DateTime, Enum
from database import Base
import datetime
import secrets

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(100))
    rol = Column(Enum("paciente", "admin", "doctor"), default="paciente")
    fecha_nacimiento = Column(String(50), nullable=True)

class Doctor(Base):
    __tablename__ = "doctores"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    especialidad = Column(String(100))
    email = Column(String(100), unique=True)
    telefono = Column(String(20))
    usuario_id = Column(Integer)
    foto_iniciales = Column(String(5))
    activo = Column(Integer, default=0)

class Cita(Base):
    __tablename__ = "citas"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer)
    doctor_id = Column(Integer)
    especialidad = Column(String(100))
    fecha = Column(String(50))
    hora = Column(String(20))
    estado = Column(Enum("pendiente", "confirmada", "cancelada"), default="pendiente")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Integer, default=0)  # 0 = not used, 1 = used