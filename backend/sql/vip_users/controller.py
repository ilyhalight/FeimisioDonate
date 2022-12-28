import time
from sql.vip_users.service import VipUsersService


class VipUsersController:
    async def add(self, account_id: int, name: str, group: str, expires: int, lastvisit: int = time.time(), sid: int = 0):
        """Добавляет привилегию для пользователя в базу данных, если у пользователя нету другой привилегии"""
        return await VipUsersService().add(account_id, name, lastvisit, sid, group, expires)

    async def get_all(self):
        """Возвращает всех пользователей с привилегиями из базы данных"""
        return await VipUsersService().get_all()

    async def get(self, account_id: int):
        """Возвращает привилегию пользователя из базы данных по айди"""
        return await VipUsersService().get(account_id)

    async def remove(self, account_id: int):
        """Удаляет привилегию пользователя из базы данных"""
        return await VipUsersService().remove(account_id)