from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from avitotech_test.balance.models import User, Balance


class UserDAL:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, id: UUID):
        created_user = User(id=id)
        self.db_session.add(created_user)
        await self.db_session.flush()  # Сначала добавляем пользователя в базу данных

        created_balance = Balance(user_id=created_user.id)  # Здесь используется user_id
        self.db_session.add(created_balance)
        await self.db_session.flush()  # Затем добавляем баланс и сохраняем изменения

        return created_user

    async def add_money(self, user_id: UUID, balance_id: UUID, amount: float):
        query = update(Balance).where(
            (Balance.balance_id == balance_id) &
            (Balance.user_id == user_id)
        ).values(balance_amount=Balance.balance_amount + amount)

        await self.db_session.execute(query)
        await self.db_session.flush()

    async def minus_money(self, user_id: UUID, balance_id: UUID, amount: float):
        # Проверяем, что user_id совпадает как в таблице User, так и в таблице Balance
        balance = select(Balance).where(
            (Balance.balance_id == balance_id) &
            (Balance.user_id == user_id)
        )

        result = await self.db_session.execute(balance)
        balance = result.scalar_one_or_none()

        if balance:
            new_balance_amount = balance.balance_amount - amount
            if new_balance_amount >= 0:
                query = update(Balance).where(
                    (Balance.balance_id == balance_id) &
                    (Balance.user_id == user_id)
                ).values(balance_amount=new_balance_amount)

                await self.db_session.execute(query)
                await self.db_session.flush()
            else:
                # Если списание приведет к отрицательному балансу, не выполняем обновление
                raise ValueError("Insufficient balance")

    async def money_transfer(self, sender_id: UUID, recipient_id: UUID, sender_balance_id: UUID,
                             recipient_balance_id: UUID, amount: float):
        sender_query = update(Balance).where(
            (Balance.balance_id == sender_balance_id) &
            (Balance.user_id == sender_id)
        ).values(balance_amount=Balance.balance_amount - amount)

        recipient_query = update(Balance).where(
            (Balance.balance_id == recipient_balance_id) &
            (Balance.user_id == recipient_id)
        ).values(balance_amount=Balance.balance_amount + amount)

        await self.db_session.execute(sender_query)
        await self.db_session.execute(recipient_query)
        await self.db_session.flush()

    async def check_balance(self, user_id: UUID, balance_id: UUID):
        balance = select(Balance).where(
            (Balance.balance_id == balance_id) &
            (Balance.user_id == user_id)
        )
        result = await self.db_session.execute(balance)
        balance_record = result.scalar_one_or_none()

        if balance_record:
            return balance_record.balance_amount
        else:
            print(f"No balance found for user_id={user_id} and balance_id={balance_id}")
            return None  # Возвращаем None, если баланс не найден
