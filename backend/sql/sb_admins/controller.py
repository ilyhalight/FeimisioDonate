from sql.sb_admins.service import SBAdminsService


class SBAdminsController:
    async def add(self, user: str, authid: str, password: str, gid: int, email: str, srv_group: str,
        expired: int = 0, validate: str = None, extraflags: int = 0, immunity: str = 0,
        srv_flags: str = None, srv_password: str = None, lastvisit: int = None, discord: str = None,
        comment: str = None, vk: str = None, tg: str = None, support: int = 0):
        """Добавляет пользователя в базу данных админов, если у пользователя нету другой привилегии
        
        Warning:
            discord, tg - это мои собственные поля добавленные в базу данных и они не входят в оригинальную базу данных MaterialAdmin или SourceBans++
        """
        return await SBAdminsService().add(user, authid, password, gid, email, validate, extraflags, immunity, srv_group, srv_flags, srv_password, lastvisit, expired, discord, comment, vk, tg, support)

    async def get_all(self):
        """Возвращает всех админов из базы данных"""
        return await SBAdminsService().get_all()

    async def get(self, account_id: int):
        """Возвращает админа из базы данных по айди"""
        return await SBAdminsService().get(account_id)

    async def remove(self, uid: int):
        """Удаляет админа из базы данных"""
        return await SBAdminsService().remove(uid)