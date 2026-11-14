"""API de eventos usada em todas as etapas do projeto."""

from datetime import date

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from app.database import make_engine, Base
from app.registrations import router
from app.db_session import get_session
from app.models import Event, Registration
from sqlalchemy.orm import Session
from sqlalchemy import select, func

class EventInput(BaseModel):
    """Dados enviados pelo cliente ao cadastrar um evento."""
    title: str
    date: date
    capacity: int

def create_app(database_url: str | None = None) -> FastAPI:
    """Cria uma API com dados isolados para cada execução ou teste."""
    app = FastAPI(title="Eventos do Trilha")
    app.include_router(router)
    if database_url is None:
        database_url = "sqlite://"
    engine = make_engine(database_url)
    app.state.engine = engine
    Base.metadata.create_all(engine)

    @app.get("/events")
    def list_events(session: Session = Depends(get_session)):
        
        eventos = session.scalars(select(Event)).all()
        lista_de_eventos = list()


        for event in eventos:
            inscritos = session.scalar(select(func.count(Registration.event_id)).where(Registration.event_id == event.id))

            event_dict = {
                "id": event.id,
                "title": event.title,
                "date": event.date,
                "capacity": event.capacity,
                "available_slots": event.capacity - inscritos,
            }

            lista_de_eventos.append(event_dict)

        return lista_de_eventos

    @app.get("/events/{event_id}")
    def get_event(event_id: int, session: Session = Depends(get_session)):
        event = session.get(Event, event_id)

        if event is None:
            raise HTTPException(status_code=404, detail="Evento não encontrado")

        inscritos = session.scalar(select(func.count(Registration.event_id)).where(Registration.event_id == event.id))

        evento = {
            "id": event.id,
            "title": event.title,
            "date": event.date,
            "capacity": event.capacity,
            "available_slots": event.capacity - inscritos,
        }

        return evento

    @app.post("/events", status_code=201)
    def create_event(data: EventInput, session: Session = Depends(get_session)):
        if data.title == "" or data.capacity <= 0:
            raise HTTPException(status_code=422, detail="Informações inválidas")

        evento = Event(title=data.title, date=data.date, capacity=data.capacity)
        session.add(evento)
        session.commit()
        session.refresh(evento)

        inscritos = session.scalar(select(func.count(Registration.event_id)).where(Registration.event_id == evento.id))

        events_dict = {
            "id": evento.id,
            "title": evento.title,
            "date": evento.date,
            "capacity": evento.capacity,
            "available_slots": evento.capacity - inscritos,
        }

        return events_dict
        # Atividade 1: valide título e capacidade, gere um ID e guarde o
        # evento em `events`. A resposta deve conter id, title, date e capacity.
        # Os testes mostram os casos de sucesso e de entrada inválida.

    return app

app = create_app("sqlite:///events.db")
