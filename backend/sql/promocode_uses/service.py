import logging

from sql.db import DefaultConnector

log = logging.getLogger('server')


class DbPromocodeUsesService:
    def __init__(self) -> None:
        self.database_sc = 'fd_promocode_uses' # Название таблицы в базе данных (для логов)

    async def init_table(self):
        """Создает таблицу в базе данных для правильной работы"""
        db = await DefaultConnector().connect()
        try:
            async with db.cursor() as cursor:
                await cursor.execute("""CREATE TABLE IF NOT EXISTS `fd_promocode_uses` (
                    `uid` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                    `key` VARCHAR(255) NOT NULL,
                    `user` VARCHAR(255),
                    `target_uid` INT NOT NULL,
                    `timestamp` BIGINT NOT NULL
                )""")
                return True
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except Exception as err:
            log.exception(f'Failed to init table in database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None

    async def add(self, key: str, user: str, target_uid: int, timestamp: int):
        """Добавляет использование промокода в базу данных

        Args:
            key: ключ промокода
            user: кто использовал промокод (steamid64)
            target_uid: что было купленоп по промокоду (uid)
            timestamp: когда был использован промокод (timestamp)

        Returns:
            True: Если удалось добавить использование промокода
            None: Если произошла ошибка
        """
        db = await DefaultConnector().connect()
        try:
            async with db.cursor() as cursor:
                await cursor.execute('INSERT INTO `fd_promocode_uses` (`key`, `user`, `target_uid`, `timestamp`) VALUES (%s, %s, %s, %s)', (key, user, target_uid, timestamp))
                await db.commit()
                return True
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except Exception as err:
            log.exception(f'Failed to add a promocode usage to the database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None

    async def get(self, key: str = None, user: str = None):
        """Возвращает использование промокода из базы данных

        Args:
            key: ключ промокода
            user: кто использовал промокод (steamid64)

        Returns:
            data: Если удалось получить данные
            None: Если произошла ошибка
        """
        db = await DefaultConnector().connect()
        try:
            async with db.cursor() as cursor:
                if key and type(key) == str:
                    await cursor.execute('SELECT * FROM `fd_promocode_uses` WHERE `key` = %s', (key, ))
                    result = await cursor.fetchall()
                elif user and type(user) == str:
                    await cursor.execute('SELECT * FROM `fd_promocode_uses` WHERE `user` = %s', (user, ))
                    result = await cursor.fetchall()
                else:
                    await cursor.execute('SELECT * FROM `fd_promocode_uses`')
                    result = await cursor.fetchall()
                return result
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except Exception as err:
            log.exception(f'Failed to get promocode usages (key: {key}, user: {user}) to the database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None

    async def remove(self, key: str):
        """Удаляет использование промокода из базы данных у всех пользователей

        Args:
            key: ключ промокода

        Returns:
            True: Если удалось удалить промокод
            None: Если произошла ошибка
        """
        db = await DefaultConnector().connect()
        try:
            async with db.cursor() as cursor:
                await cursor.execute('DELETE FROM `fd_promocode_uses` WHERE `key` = %s', (key, ))
                await db.commit()
                return True
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except Exception as err:
            log.exception(f'Failed to remove promocode usages to the database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None