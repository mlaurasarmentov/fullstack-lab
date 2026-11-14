"""Rota de inscrição a completar na atividade 3."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models import Registration, User, Event
from app.db_session import get_session


router = APIRouter()


class RegistrationInput(BaseModel):
    user_id: int


@router.post("/events/{event_id}/registrations", status_code=201)
def register(event_id: int, data: RegistrationInput, session: Session = Depends(get_session)):
    evento = session.get(Event, event_id)

    if evento is None:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    usuario = session.get(User, data.user_id)

    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if session.scalar(select(Registration.event_id).where(Registration.event_id == event_id, \
        Registration.user_id == data.user_id)) is not None:
        raise HTTPException(status_code=409, detail="Já inscrito")

    if session.scalar(select(func.count(Registration.event_id)).where(Registration.event_id == event_id)) >= evento.capacity:
        raise HTTPException(status_code=409, detail="Evento lotado")

    registro = Registration(event_id=event_id, user_id=data.user_id)
    session.add(registro)
    session.commit()

    return {"event_id": event_id, "user_id": data.user_id}

    # Atividade 3: verifique evento, usuário, duplicidade e vagas. Só então
    # grave Registration e responda com event_id e user_id.
