from sqlalchemy import Column, Integer, String, DateTime, Enum
from database import Base
import datetime

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(100))
    rol = Column(Enum("paciente", "admin", "doctor"), default="paciente")

class Doctor(Base):
    __tablename__ = "doctores"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    especialidad = Column(String(100))
    email = Column(String(100), unique=True)
    telefono = Column(String(20))
    usuario_id = Column(Integer)
    foto_iniciales = Column(String(5))

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