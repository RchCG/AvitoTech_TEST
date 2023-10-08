from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    id: UUID = Field(default_factory=uuid4)


class BalanceBase(BaseModel):
    balance_id: UUID = Field(default_factory=uuid4)
    balance_amount: float = Field(default=0, gt=-1)
