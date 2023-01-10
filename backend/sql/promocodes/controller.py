from sql.promocodes.service import DbPromocodesService


class DbPromocodesController:
    async def init(self):
        """Создаёт таблицу в базе данных, если она не существует"""
        return await DbPromocodesService().init_table()

    async def add(self, key: str, author: str, discount: int, expires: int, uses: int, min_price: int, max_price: int):
        """Добавляет промокод в базу данных"""
        return await DbPromocodesService().add(key, author, discount, expires, uses, min_price, max_price)

    async def get_all(self):
        """Возвращает все промокоды из базы данных"""
        return await DbPromocodesService().get()

    async def get_by_key(self, key: str):
        """Возвращает промокод из базы данных по ключу"""
        return await DbPromocodesService().get(key = key)

    async def get_by_author(self, author: str):
        """Возвращает промокод из базы данных по автору
        
            Args:
                author: автора промокода (steamid64)
        """
        return await DbPromocodesService().get(author = author)

    async def remove(self, key: str):
        """Удаляет промокод из базы данных"""
        return await DbPromocodesService().remove(key)