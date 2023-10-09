from uuid import UUID

from avitotech_test.balance.service import UserDAL


async def register_new_user(id: UUID, db):
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            new_user = await user_dal.create_user(id=id)
            return new_user


async def replenishment(user_id: UUID, balance_id: UUID, amount: float, db):
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            money_transfer = await user_dal.add_money(user_id=user_id, balance_id=balance_id, amount=amount)
            return money_transfer


async def charge_off(user_id: UUID, balance_id: UUID, amount: float, db):
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            money_transfer = await user_dal.minus_money(user_id=user_id, balance_id=balance_id, amount=amount)
            return money_transfer


async def checking_balance(user_id: UUID, balance_id: UUID, db):
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            checking = await user_dal.check_balance(user_id=user_id, balance_id=balance_id)
            return checking


async def transfer_money(sender_id: UUID, sender_balance_id: UUID, recipient_id: UUID, recipient_balance_id: UUID,
                        amount: float, db):
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            transfer = await user_dal.money_transfer(sender_id=sender_id, sender_balance_id=sender_balance_id,
                                                     recipient_id=recipient_id,
                                                     recipient_balance_id=recipient_balance_id, amount=amount)
            return transfer