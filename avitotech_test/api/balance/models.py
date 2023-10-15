import uuid
from sqlalchemy import Column, Integer, String, UUID, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True)
    balance: Mapped["Balance"] = relationship(back_populates="user", uselist=False)

class Balance(Base):
    __tablename__ = "balances"

    balance_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    balance_amount: Mapped[float] = mapped_column(default=0, nullable=False)
    user: Mapped["User"] = relationship(back_populates="balance", uselist=False)

