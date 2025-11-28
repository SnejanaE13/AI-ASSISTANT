from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Text,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base

class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True, nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    second_name = Column(String(30), nullable=True)
    role = Column(String(20), nullable=False)  # 'student' или 'teacher'
    password_hash = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    sessions = relationship("Session", back_populates="user")
    messages = relationship("Message", back_populates="user")


class Session(Base):
    __tablename__ = "session"
    session_id = Column(String, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session")


class Message(Base):
    __tablename__ = "message"
    message_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    session_id = Column(String, ForeignKey("session.session_id"), nullable=False)
    sender_type = Column(String(10), nullable=False)  # 'user' или 'ai'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    prompt_id = Column(Integer, ForeignKey("prompt.prompt_id"), nullable=True)
    user = relationship("User", back_populates="messages")
    session = relationship("Session", back_populates="messages")
    prompt = relationship("Prompt", back_populates="messages")


class Prompt(Base):
    __tablename__ = "prompt"
    prompt_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)
    messages = relationship("Message", back_populates="prompt")

 # НОВАЯ МОДЕЛЬ: Сохранение состояний экранов пользователя
class UserScreenState(Base):
     __tablename__ = "user_screen_state"
     
     state_id = Column(Integer, primary_key=True, index=True)
     user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
     screen_name = Column(String(50), nullable=False)  # Например: 'student-dashboard', 'teacher-analysis'
     state_data = Column(Text, nullable=False)  # JSON данные состояния
     last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc))
     
     # Связь с пользователем
     user = relationship("User")
 
     # Уникальный индекс: один пользователь - одно состояние на экран
     __table_args__ = (UniqueConstraint('user_id', 'screen_name', name='uq_user_screen'),)