from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

@router.get("/")
def obtener_doctores(db: Session = Depends(get_db)):
    doctores = db.query(models.Doctor).filter(models.Doctor.activo == 1).all()
    return [{
        "id": d.id,
        "nombre": d.nombre,
        "especialidad": d.especialidad,
        "email": d.email,
        "telefono": d.telefono,
        "foto_iniciales": d.foto_iniciales,
    } for d in doctores]

@router.get("/todos")
def obtener_todos_doctores(db: Session = Depends(get_db)):
    doctores = db.query(models.Doctor).all()
    return [{
        "id": d.id,
        "nombre": d.nombre,
        "especialidad": d.especialidad,
        "email": d.email,
        "telefono": d.telefono,
        "foto_iniciales": d.foto_iniciales,
        "activo": d.activo,
    } for d in doctores]

@router.put("/{doctor_id}/toggle-activo")
def toggle_activo_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    doctor.activo = 1 if doctor.activo == 0 else 0
    db.commit()
    return {"mensaje": f"Estado del doctor actualizado a {doctor.activo}"}

@router.get("/{doctor_id}/horarios")
def horarios_disponibles(doctor_id: int, fecha: str, db: Session = Depends(get_db)):
    todos_los_horarios = [
        "07:00", "07:30", "08:00", "08:30", "09:00", "09:30",
        "10:00", "10:30", "11:00", "11:30", "14:00", "14:30",
        "15:00", "15:30", "16:00", "16:30", "17:00"
    ]
    ocupados = db.query(models.Cita).filter(
        models.Cita.doctor_id == doctor_id,
        models.Cita.fecha == fecha,
        models.Cita.estado != "cancelada"
    ).all()
    horas_ocupadas = [c.hora for c in ocupados]
    disponibles = [h for h in todos_los_horarios if h not in horas_ocupadas]
    return {"disponibles": disponibles, "ocupados": horas_ocupadas}