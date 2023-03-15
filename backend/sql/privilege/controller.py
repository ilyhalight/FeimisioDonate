from sql.privilege.service import DbPrivilegeService


class DbPrivilegeController:
    async def init(self):
        """Создаёт таблицу в базе данных, если она не существует"""
        return await DbPrivilegeService().init_table()

    async def add_privilege(self, name: str, price: int, link: str, duration: int, discount: int, short_description: str, disabled: bool = False):
        """Добавляет привилегию в базу данных"""
        return await DbPrivilegeService().add_privilege(name, price, link, duration, discount, short_description, disabled)

    async def get_all(self):
        """Возвращает все привилегии из базы данных"""
        return await DbPrivilegeService().get()

    async def get_by_uid(self, uid: int):
        """Возвращает привилегию из базы данных по айди"""
        return await DbPrivilegeService().get(uid = uid)

    async def get_by_name(self, name: str):
        """Возвращает привилегию из базы данных по имени"""
        return await DbPrivilegeService().get(name = name)

    async def get_by_link(self, link: str):
        """Возвращает привилегию из базы данных по имени"""
        return await DbPrivilegeService().get(link = link)

    async def add_discount(self, uid: int, discount: int):
        """Добавляет скидку на привилегию из базы данных"""
        return await DbPrivilegeService().add_discount(uid, discount)

    async def remove(self, uid: int):
        """Удаляет привилегию из базы данных"""
        return await DbPrivilegeService().remove_privilege(uid)