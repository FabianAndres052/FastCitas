from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
import models

router = APIRouter()

class CitaData(BaseModel):
    paciente_id: int
    doctor_id: int
    especialidad: str
    fecha: str
    hora: str

@router.post("/")
def crear_cita(data: CitaData, db: Session = Depends(get_db)):
    conflicto = db.query(models.Cita).filter(
        models.Cita.doctor_id == data.doctor_id,
        models.Cita.fecha == data.fecha,
        models.Cita.hora == data.hora,
        models.Cita.estado != "cancelada"
    ).first()
    if conflicto:
        raise HTTPException(status_code=400, detail="Ese doctor ya tiene una cita en ese horario")
    
    cita = models.Cita(
        paciente_id=data.paciente_id,
        doctor_id=data.doctor_id,
        especialidad=data.especialidad,
        fecha=data.fecha,
        hora=data.hora
    )
    db.add(cita)
    db.commit()
    db.refresh(cita)
    return cita

@router.get("/paciente/{paciente_id}")
def citas_paciente(paciente_id: int, db: Session = Depends(get_db)):
    try:
        query_res = db.query(models.Cita, models.Doctor).join(
            models.Doctor, models.Cita.doctor_id == models.Doctor.id, isouter=True
        ).filter(models.Cita.paciente_id == paciente_id).all()
        resultado = []
        for cita, doctor in query_res:
            resultado.append({
                "id": cita.id,
                "especialidad": cita.especialidad,
                "fecha": cita.fecha,
                "hora": cita.hora,
                "estado": cita.estado,
                "doctor_nombre": doctor.nombre if doctor else "Sin asignar",
                "doctor_iniciales": doctor.foto_iniciales if doctor else "??",
            })
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener las citas del paciente")

@router.get("/doctor/{doctor_id}")
def citas_doctor(doctor_id: int, db: Session = Depends(get_db)):
    try:
        query_res = db.query(models.Cita, models.Usuario).join(
            models.Usuario, models.Cita.paciente_id == models.Usuario.id, isouter=True
        ).filter(models.Cita.doctor_id == doctor_id).all()
        resultado = []
        for cita, paciente in query_res:
            resultado.append({
                "id": cita.id,
                "especialidad": cita.especialidad,
                "fecha": cita.fecha,
                "hora": cita.hora,
                "estado": cita.estado,
                "paciente_nombre": paciente.nombre if paciente else "Desconocido",
                "paciente_email": paciente.email if paciente else "N/A",
            })
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener las citas del doctor")

@router.get("/")
def todas_las_citas(db: Session = Depends(get_db)):
    try:
        query_res = db.query(models.Cita, models.Doctor, models.Usuario).join(
            models.Doctor, models.Cita.doctor_id == models.Doctor.id, isouter=True
        ).join(
            models.Usuario, models.Cita.paciente_id == models.Usuario.id, isouter=True
        ).all()
        resultado = []
        for cita, doctor, paciente in query_res:
            resultado.append({
                "id": cita.id,
                "paciente_id": cita.paciente_id,
                "paciente_nombre": paciente.nombre if paciente else "Desconocido",
                "doctor_id": cita.doctor_id,
                "doctor_nombre": doctor.nombre if doctor else "Sin asignar",
                "especialidad": cita.especialidad,
                "fecha": cita.fecha,
                "hora": cita.hora,
                "estado": cita.estado,
            })
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener la lista de todas las citas")

@router.put("/{cita_id}/estado")
def actualizar_estado(cita_id: int, estado: str, db: Session = Depends(get_db)):
    cita = db.query(models.Cita).filter(models.Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    cita.estado = estado
    db.commit()
    return {"mensaje": "Estado actualizado"}

@router.delete("/{cita_id}")
def eliminar_cita(cita_id: int, db: Session = Depends(get_db)):
    cita = db.query(models.Cita).filter(models.Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    db.delete(cita)
    db.commit()
    return {"mensaje": "Cita eliminada"}