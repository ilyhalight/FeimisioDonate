import logging

from pymysql.err import IntegrityError
from aiogram.utils.markdown import escape_md

from sql.db import SBConnector
from logger.masslog import MassLog

log = logging.getLogger('server')


class SBAdminsService:
    def __init__(self) -> None:
        self.database_sc = 'sb_admins' # Название таблицы в базе данных (для логов)

    async def add(self, user: str, authid: str, password: str, gid: int, email: str,
        validate: str, extraflags: int, immunity: str,
        srv_group: str, srv_flags: str, srv_password: str, lastvisit: int, expired: int, discord: str,
        comment: str, vk: str, tg: str, support: int):
        """Добавляет админа в базу данных

        Args:
            user (str): Имя админа
            authid (str): SteamID64 админа
            password (str): Пароль админа
            gid (int): Группа админа
            email (str): Email админа
            validate (str): Ключ активации
            extraflags (int): Дополнительные флаги
            immunity (str): Иммунитет
            srv_group (str): Группа сервера админа
            srv_flags (str): Флаги сервера
            srv_password (str): Пароль сервера
            lastvisit (int): Последний визит
            expired (int): Время истечения привилегии
            discord (str): Discord админа
            comment (str): Комментарий админа
            vk (str): VK админа
            tg (str): Telegram админа
            support (int): Поддержка

        Returns:
            True: Если удалось добавить админа
            None: Если произошла ошибка
        """
        db = await SBConnector().connect()
        try:
            async with db.cursor() as cursor:
                await cursor.execute('INSERT INTO `sb_admins` (`user`, `authid`, `password`, `gid`, `email`, `validate`, `extraflags`, `immunity`, `srv_group`, `srv_flags`, `srv_password`, `lastvisit`, `expired`, `discord`, `comment`, `vk`, `tg`, `support`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (user, authid, password, gid, email, validate, extraflags, immunity, srv_group, srv_flags, srv_password, lastvisit, expired, discord, comment, vk, tg, support))
                await db.commit()
                return True
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except IntegrityError as err:
            MassLog().error(f'Игрок с **{escape_md(authid)}** уже есть в базе данных MaterialAdmin')
            return None
        except Exception as err:
            log.exception(f'Failed to add a admin to the database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None

    async def get_all(self):
        """Возвращает всех админов из базы данных

        Returns:
            data: Если удалось получить данные
            None: Если произошла ошибка
        """
        db = await SBConnector().connect()
        try:
            async with db.cursor() as cursor:
                await cursor.execute('SELECT * FROM `sb_admins`')
                result = await cursor.fetchall()
                return result
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except Exception as err:
            log.exception(f'Failed to get all admin from the database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None

    async def get(self, authid: int):
        """Возвращает админа из базы данных

        Args:
            authid: id аккаунта (steamID (STEAM_0:...))

        Returns:
            data: Если удалось получить данные
            None: Если произошла ошибка
        """
        db = await SBConnector().connect()
        try:
            async with db.cursor() as cursor:
                await cursor.execute('SELECT * FROM `sb_admins` WHERE `account_id` = %s', (authid, ))
                result = await cursor.fetchone()
                return result
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except Exception as err:
            log.exception(f'Failed to get admin ({authid}) from the database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None

    async def remove(self, authid: int):
        """Удаляет админа из базы данных

        Args:
            authid: id аккаунта (steamID (STEAM_0:...))

        Returns:
            True: Если удалось удалить админа
            None: Если произошла ошибка
        """
        db = await SBConnector().connect()
        try:
            async with db.cursor() as cursor:
                await cursor.execute('DELETE FROM `sb_admins` WHERE `authid` = %s', (authid, ))
                await db.commit()
                return True
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except Exception as err:
            log.exception(f'Failed to remove admin to the database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None