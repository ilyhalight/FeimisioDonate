from sql.privillege.service import DbPrivillegeService


class DbPrivillegeController:
    async def init(self):
        """Создаёт таблицу в базе данных, если она не существует"""
        return await DbPrivillegeService().init_table()

    async def add_privillege(self, name: str, price: int, link: str, duration: int, discount: int, short_description: str, description: str):
        """Добавляет привилегию в базу данных"""
        return await DbPrivillegeService().add_privillege(name, price, link, duration, discount, short_description, description)

    async def get_all(self):
        """Возвращает все привилегии из базы данных"""
        return await DbPrivillegeService().get()

    async def get_by_uid(self, uid: int):
        """Возвращает привилегию из базы данных по айди"""
        return await DbPrivillegeService().get(uid = uid)

    async def get_by_name(self, name: str):
        """Возвращает привилегию из базы данных по имени"""
        return await DbPrivillegeService().get(name = name)

    async def get_by_link(self, link: str):
        """Возвращает привилегию из базы данных по имени"""
        return await DbPrivillegeService().get(link = link)

    async def add_discount(self, uid: int, discount: int):
        """Добавляет скидку на привилегию из базы данных"""
        return await DbPrivillegeService().add_discount(uid, discount)

    async def remove(self, uid: int):
        """Удаляет привилегию из базы данных"""
        return await DbPrivillegeService().remove_privillege(uid)