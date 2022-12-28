import logging

from sql.db import VIPUsersConnector

log = logging.getLogger('server')


class VipUsersService:
    def __init__(self) -> None:
        self.database_sc = 'vip_users' # Название таблицы в базе данных (для логов)

    async def add(self, account_id: int, name: str, lastvisit: int, sid: int, group: str, expires: int):
        """Добавляет привилегию для пользователя в базу данных

        Args:
            account_id: id аккаунта (steamID3 без буквы 'U' в начале и спец. символов)
            name: ник аккаунта
            lastvisit: последний вход на сервер
            sid: id сервера
            group: имя привилегии
            expires: дата истечения привилегии в формате timestamp

        Returns:
            True: Если удалось добавить привилегию
            None: Если произошла ошибка
        """
        db = await VIPUsersConnector().connect()
        try:
            async with db.cursor() as cursor:
                await cursor.execute('INSERT INTO `vip_users` (`account_id`, `name`, `lastvisit`, `sid`, `group`, `expires`) VALUES (%s, %s, %s, %s, %s, %s)', (account_id, name, lastvisit, sid, group, expires))
                await db.commit()
                return True
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except Exception as err:
            log.exception(f'Failed to add a privillege to the database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None

    async def get_all(self):
        """Возвращает все привилегии из базы данных

        Returns:
            data: Если удалось получить данные
            None: Если произошла ошибка
        """
        db = await VIPUsersConnector().connect()
        try:
            async with db.cursor() as cursor:
                await cursor.execute('SELECT * FROM `vip_users`')
                result = await cursor.fetchall()
                return result
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except Exception as err:
            log.exception(f'Failed to get all privilleges from the database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None

    async def get(self, account_id: int):
        """Возвращает привилегию из базы данных

        Args:
            account_id: id аккаунта (steamID3 без буквы 'U' в начале и спец. символов)

        Returns:
            data: Если удалось получить данные
            None: Если произошла ошибка
        """
        db = await VIPUsersConnector().connect()
        try:
            async with db.cursor() as cursor:
                await cursor.execute('SELECT * FROM `vip_users` WHERE `account_id` = %s', (account_id,))
                result = await cursor.fetchone()
                return result
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except Exception as err:
            log.exception(f'Failed to get privilleges ({account_id}) from the database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None

    async def remove(self, account_id: int):
        """Удаляет привилегию из базы данных

        Args:
            account_id: id аккаунта (steamID3 без буквы 'U' в начале и спец. символов)

        Returns:
            True: Если удалось удалить привилегию
            None: Если произошла ошибка
        """
        db = await VIPUsersConnector().connect()
        try:
            async with db.cursor() as cursor:
                await cursor.execute('DELETE FROM `vip_users` WHERE `account_id` = %s', (account_id, ))
                await db.commit()
                return True
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except Exception as err:
            log.exception(f'Failed to remove user privillege to the database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None