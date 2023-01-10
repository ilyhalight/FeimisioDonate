import logging

from sql.db import DefaultConnector

log = logging.getLogger('server')


class DbPromocodesService:
    def __init__(self) -> None:
        self.database_sc = 'fd_promocodes' # Название таблицы в базе данных (для логов)

    async def init_table(self):
        """Создает таблицу в базе данных для правильной работы"""
        db = await DefaultConnector().connect()
        try:
            async with db.cursor() as cursor:
                await cursor.execute("""CREATE TABLE IF NOT EXISTS `fd_promocodes` (
                    `uid` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                    `key` VARCHAR(255) NOT NULL,
                    `author` VARCHAR(255),
                    `discount` INT NOT NULL,
                    `expires` INT NOT NULL DEFAULT 0,
                    `uses` INT NOT NULL DEFAULT 0,
                    `min_price` INT NOT NULL DEFAULT 0,
                    `max_price` INT NOT NULL DEFAULT 999999
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

    async def add(self, key: str, author: str, discount: int, expires: int, uses: int, min_price: int, max_price: int):
        """Добавляет промокод в базу данных

        Args:
            key: ключ промокода
            author: автор промокода (steamid64)
            discount: скидка по промокоду
            expires: время истечения промокода (timestamp)
            uses: количество использований промокода
            min_price: минимальная цена для применения промокода
            max_price: максимальная цена для применения промокода

        Returns:
            True: Если удалось добавить промокод
            None: Если произошла ошибка
        """
        db = await DefaultConnector().connect()
        try:
            async with db.cursor() as cursor:
                await cursor.execute('INSERT INTO `fd_promocodes` (`key`, `author`, `discount`, `expires`, `uses`, `min_price`, `max_price`) VALUES (%s, %s, %s, %s, %s, %s, %s)', (key, author, discount, expires, uses, min_price, max_price))
                await db.commit()
                return True
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except Exception as err:
            log.exception(f'Failed to add a promocode to the database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None

    async def get(self, key: str = None, author: str = None):
        """Возвращает промокод из базы данных

        Args:
            key: ключ промокода
            author: автор промокода (steamid64)

        Returns:
            data: Если удалось получить данные
            None: Если произошла ошибка
        """
        db = await DefaultConnector().connect()
        try:
            async with db.cursor() as cursor:
                if key and type(key) == str:
                    await cursor.execute('SELECT * FROM `fd_promocodes` WHERE `key` = %s', (key, ))
                    result = await cursor.fetchone()
                elif author and type(author) == str:
                    await cursor.execute('SELECT * FROM `fd_promocodes` WHERE `author` = %s', (author, ))
                    result = await cursor.fetchone()
                else:
                    await cursor.execute('SELECT * FROM `fd_promocodes`')
                    result = await cursor.fetchall()
                return result
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except Exception as err:
            log.exception(f'Failed to get promocode (key: {key}, author: {author}) to the database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None

    async def remove(self, key: str):
        """Удаляет промокод из базы данных

        Args:
            key: ключ промокода

        Returns:
            True: Если удалось удалить промокод
            None: Если произошла ошибка
        """
        db = await DefaultConnector().connect()
        try:
            async with db.cursor() as cursor:
                await cursor.execute('DELETE FROM `fd_promocodes` WHERE `key` = %s', (key, ))
                await db.commit()
                return True
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except Exception as err:
            log.exception(f'Failed to remove promocode to the database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None