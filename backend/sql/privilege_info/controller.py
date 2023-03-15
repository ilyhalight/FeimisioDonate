from sql.privilege_info.service import DbPrivilegeInfoService


class DbPrivilegeInfoController:
    async def init(self):
        """Создаёт таблицу в базе данных, если она не существует"""
        return await DbPrivilegeInfoService().init_table()

    async def add_privilege(self, link: str, name: str, desc: str, img_link: str = None, is_big_img: bool = None, img_reverse_side: bool = None):
        """Добавляет информацию о привилегии в базу данных"""
        return await DbPrivilegeInfoService().add(link, name, desc, img_link, is_big_img, img_reverse_side)

    async def get_all(self):
        """Возвращает всю информацию о привилегиях из базы данных"""
        return await DbPrivilegeInfoService().get()

    async def get(self, link: str):
        """Возвращает всю информацию о привилегии из базы данных по ссылке"""
        return await DbPrivilegeInfoService().get(link)

    async def remove(self, uid: int):
        """Удаляет информацию о привилегии из базы данных"""
        return await DbPrivilegeInfoService().remove(uid)