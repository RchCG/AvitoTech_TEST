from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from avitotech_test.balance.router import register_new_user, replenishment, charge_off, checking_balance, transfer_money
from avitotech_test.db.session import get_db

balance_router = APIRouter(prefix="/api/v1/balance", tags=["UserBalance"])


@balance_router.post("/create_user", tags=["UserBalance"], summary="Создание пользователя", status_code=201)
async def create_user(user_id: UUID = None, db: AsyncSession = Depends(get_db)):
    return await register_new_user(user_id, db)


@balance_router.post("/enrollment", tags=["UserBalance"], summary="Зачисление средств", status_code=200)
async def enrollment(user_id: UUID, balance_id: UUID, amount: float, db: AsyncSession = Depends(get_db)):
    query = await replenishment(user_id=user_id, balance_id=balance_id, amount=amount, db=db)
    return {f"Баланс счёта {balance_id} пополнен на: {amount} RUB"}


@balance_router.post("/write_off", tags=["UserBalance"], summary="Списание средств", status_code=200)
async def write_off(user_id: UUID, balance_id: UUID, amount: float, db: AsyncSession = Depends(get_db)):
    query = await charge_off(user_id=user_id, balance_id=balance_id, amount=amount, db=db)
    return {f"C баланса счёта {balance_id} списано: {amount} RUB"}


@balance_router.post("/remittance", tags=["UserBalance"], summary="Перевод средств другому клиенту", status_code=200)
async def remittance(sender_id: UUID, sender_balance_id: UUID, recipient_id: UUID, recipient_balance_id: UUID,
                     amount: float, db: AsyncSession = Depends(get_db)):
    query = await transfer_money(sender_id=sender_id, sender_balance_id=sender_balance_id,
                                 recipient_id=recipient_id,
                                 recipient_balance_id=recipient_balance_id, amount=amount, db=db)
    return {f"Перевод с кошелька {sender_balance_id} на {recipient_balance_id} произведён успешно"}


@balance_router.get("/current_balance", tags=["UserBalance"], summary="Просмотреть текущий баланс", status_code=200)
async def current_balance(user_id: UUID, balance_id: UUID, db: AsyncSession = Depends(get_db)):
    query = await checking_balance(user_id=user_id, balance_id=balance_id, db=db)
    return {f"Текущий баланс составляет {query}"}
