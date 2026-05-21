from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Cita
from pydantic import BaseModel

router = APIRouter()

class CitaSchema(BaseModel):
    paciente_id: int
    especialidad: str
    fecha: str
    hora: str

@router.get("/")
def get_citas(db: Session = Depends(get_db)):
    return db.query(Cita).all()

@router.get("/paciente/{paciente_id}")
def get_citas_paciente(paciente_id: int, db: Session = Depends(get_db)):
    return db.query(Cita).filter(Cita.paciente_id == paciente_id).all()

@router.post("/")
def crear_cita(data: CitaSchema, db: Session = Depends(get_db)):
    cita = Cita(**data.model_dump())
    db.add(cita)
    db.commit()
    db.refresh(cita)
    return cita

@router.put("/{cita_id}/estado")
def actualizar_estado(cita_id: int, estado: str, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    cita.estado = estado
    db.commit()
    return cita

@router.delete("/{cita_id}")
def eliminar_cita(cita_id: int, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    db.delete(cita)
    db.commit()
    return {"mensaje": "Cita eliminada"}