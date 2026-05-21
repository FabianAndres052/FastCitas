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
        citas = db.query(models.Cita).filter(models.Cita.paciente_id == paciente_id).all()
        resultado = []
        for c in citas:
            doctor = db.query(models.Doctor).filter(models.Doctor.id == c.doctor_id).first()
            resultado.append({
                "id": c.id,
                "especialidad": c.especialidad,
                "fecha": c.fecha,
                "hora": c.hora,
                "estado": c.estado,
                "doctor_nombre": doctor.nombre if doctor else "Sin asignar",
                "doctor_iniciales": doctor.foto_iniciales if doctor else "??",
            })
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def todas_las_citas(db: Session = Depends(get_db)):
    try:
        citas = db.query(models.Cita).all()
        resultado = []
        for c in citas:
            doctor = None
            paciente = None
            try:
                doctor = db.query(models.Doctor).filter(models.Doctor.id == c.doctor_id).first()
                paciente = db.query(models.Usuario).filter(models.Usuario.id == c.paciente_id).first()
            except:
                pass
            resultado.append({
                "id": c.id,
                "paciente_id": c.paciente_id,
                "paciente_nombre": paciente.nombre if paciente else "Desconocido",
                "doctor_id": c.doctor_id,
                "doctor_nombre": doctor.nombre if doctor else "Sin asignar",
                "especialidad": c.especialidad,
                "fecha": c.fecha,
                "hora": c.hora,
                "estado": c.estado,
            })
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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