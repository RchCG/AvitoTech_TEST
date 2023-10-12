from uuid import UUID

from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from avitotech_test.api.balance.models import User, Balance


class UserDAL:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, id: UUID):
        try:
            created_user = User(id=id)
            self.db_session.add(created_user)
            await self.db_session.flush()  # Сначала добавляем пользователя в базу данных

            created_balance = Balance(user_id=created_user.id)
            self.db_session.add(created_balance)
            await self.db_session.flush()  # Затем добавляем баланс и сохраняем изменения

            return created_user
        except Exception as e:
            return None

    async def add_money(self, user_id: UUID, balance_id: UUID, amount: float):
        query = update(Balance).where(and_(Balance.balance_id == balance_id, Balance.user_id == user_id)).values(
            balance_amount=Balance.balance_amount + amount)

        try:
            await self.db_session.execute(query)
            await self.db_session.flush()
            return True
        except Exception as e:
            return False

    async def minus_money(self, user_id: UUID, balance_id: UUID, amount: float):
        try:
            balance = select(Balance).where(and_(
                Balance.balance_id == balance_id, Balance.user_id == user_id))

            result = await self.db_session.execute(balance)
            balance = result.scalar_one_or_none()

            if balance:
                new_balance_amount = balance.balance_amount - amount
                if new_balance_amount >= 0:
                    query = update(Balance).where(and_(
                        Balance.balance_id == balance_id, Balance.user_id == user_id)).values(
                        balance_amount=new_balance_amount)

                    await self.db_session.execute(query)
                    await self.db_session.flush()
                    return True
                else:
                    return False
        except Exception as e:
            return False

    async def money_transfer(self, sender_id: UUID, recipient_id: UUID, sender_balance_id: UUID,
                             recipient_balance_id: UUID, amount: float):
        try:
            sender_query = select(Balance).where(
                and_(Balance.balance_id == sender_balance_id, Balance.user_id == sender_id))

            recipient_query = select(Balance).where(
                and_(Balance.balance_id == recipient_balance_id, Balance.user_id == recipient_id))

            sender_result = await self.db_session.execute(sender_query)
            recipient_result = await self.db_session.execute(recipient_query)
            sender_balance = sender_result.scalar_one_or_none()
            recipient_balance = recipient_result.scalar_one_or_none()

            if sender_balance:
                if sender_balance.balance_amount - amount >= 0:
                    new_sender_amount = sender_balance.balance_amount - amount
                    sender_query = update(Balance).where(
                        and_(Balance.balance_id == sender_balance_id, Balance.user_id == sender_id)).values(
                        balance_amount=new_sender_amount)

                    new_recipent_amount = recipient_balance.balance_amount + amount
                    recipient_query = update(Balance).where(
                        and_(Balance.balance_id == recipient_balance_id, Balance.user_id == recipient_id)).values(
                        balance_amount=new_recipent_amount)

                    await self.db_session.execute(sender_query)
                    await self.db_session.execute(recipient_query)
                    await self.db_session.flush()

                    return True
                else:
                    return False
        except Exception as e:
            return False

    async def check_balance(self, user_id: UUID, balance_id: UUID):
        try:
            balance = select(Balance).where(and_(Balance.balance_id == balance_id, Balance.user_id == user_id))
            result = await self.db_session.execute(balance)
            balance_record = result.scalar_one_or_none()

            return balance_record.balance_amount

        except Exception as e:
            return False
