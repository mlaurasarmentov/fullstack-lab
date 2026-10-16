"""Modelos relacionais que serão completados na atividade 2."""

from sqlalchemy import Integer, String, Date, CheckConstraint, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from datetime import date


class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    date: Mapped[date] = mapped_column(Date)
    capacity: Mapped[int] = mapped_column(Integer)
    __table_args__ = (CheckConstraint("capacity>0"),)
    # Complete os campos title, date e capacity e suas restrições.


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    # Complete os campos name e email.


class Registration(Base):
    __tablename__ = "registrations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("events.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    __table_args__ = (UniqueConstraint("event_id", "user_id"),)
    # Relacione event_id e user_id às tabelas corretas e impeça duplicatas.
