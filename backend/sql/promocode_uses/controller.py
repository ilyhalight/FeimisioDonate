from sql.promocode_uses.service import DbPromocodeUsesService


class DbPromocodeUsesController:
    async def init(self):
        """Создаёт таблицу в базе данных, если она не существует"""
        return await DbPromocodeUsesService().init_table()

    async def add(self, key: str, user: str, target_uid: int, timestamp: int):
        """Добавляет использование промокода в базу данных"""
        return await DbPromocodeUsesService().add(key, user, target_uid, timestamp)

    async def get_all(self):
        """Возвращает все использования промокода из базы данных"""
        return await DbPromocodeUsesService().get()

    async def get_by_key(self, key: str):
        """Возвращает использование промокода из базы данных по ключу"""
        return await DbPromocodeUsesService().get(key = key)

    async def get_by_user(self, user: str):
        """Возвращает использование промокода из базы данных по пользователю
        
            Args:
                user: кто использовал промокод (steamid64)
        """
        return await DbPromocodeUsesService().get(user = user)

    async def remove(self, key: str):
        """Удаляет промокод из базы данных"""
        return await DbPromocodeUsesService().remove(key)