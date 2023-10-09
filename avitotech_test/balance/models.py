import uuid
from sqlalchemy import Column, Integer, String, UUID, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):  # Модель пользователя в БД
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    balance = relationship("Balance", uselist=False, back_populates="user")


class Balance(Base):  # Модель баланса пользователя в бд
    __tablename__ = "balances"

    balance_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    user_id = Column(UUID, ForeignKey(User.id, ondelete="CASCADE"))
    balance_amount = Column(Float, default=0, nullable=False)
    user = relationship("User", back_populates="balance")
