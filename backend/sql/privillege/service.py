import logging

from sql.db import DefaultConnector

log = logging.getLogger('server')


class DbPrivillegeService:
    def __init__(self) -> None:
        self.database_sc = 'fd_privillege' # Название таблицы в базе данных (для логов)

    async def init_table(self):
        """Создает таблицу в базе данных для правильной работы"""
        db = await DefaultConnector().connect()
        try:
            async with db.cursor() as cursor:
                await cursor.execute("""CREATE TABLE IF NOT EXISTS `fd_privillege` (
                    `uid` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                    `name` VARCHAR(255) NOT NULL,
                    `price` INT NOT NULL,
                    `link` VARCHAR(255) NOT NULL,
                    `duration` INT NOT NULL,
                    `discount` INT NOT NULL,
                    `short_description` VARCHAR(512),
                    `description` VARCHAR(3000)
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

    async def add_privillege(self, name: str, price: int, link: str, duration: int, discount: int, short_description: str, description: str):
        """Добавляет привилегию в базу данных

        Args:
            name: имя привилегии
            price: цена привилегии
            link: ссылка на описание привилегии
            duration: продолжительность привилегии (в часах)
            discount: скидка на привилегию
            short_description: короткое описание привилегии ("Вы получите")
            description: описание блока страницы с описанием привилегии

        Returns:
            True: Если удалось добавить привилегию
            None: Если произошла ошибка
        """
        db = await DefaultConnector().connect()
        try:
            async with db.cursor() as cursor:
                await cursor.execute('INSERT INTO `fd_privillege` (`name`, `price`, `link`, `duration`, `discount`, `short_description`, `description`) VALUES (%s, %s, %s, %s, %s, %s, %s)', (name, price, link, duration, discount, short_description, description))
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

    async def add_discount(self, uid: int, discount: int):
        """Добавляет скидку на привилегию в базу данных

        Args:
            uid: id привилегии
            discount: скидка на привилегию

        Returns:
            True: Если удалось добавить скидку
            None: Если произошла ошибка
        """
        db = await DefaultConnector().connect()
        try:
            async with db.cursor() as cursor:
                await cursor.execute('UPDATE `fd_privillege` SET `discount` = %s WHERE `uid` = %s', (discount, uid))
                await db.commit()
                return True
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except Exception as err:
            log.exception(f'Failed to add a discount for privillege (uid: {uid}) to the database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None

    async def get(self, uid: int = None, name: str = None, link: str = None):
        """Возвращает привилегию из базы данных

        Args:
            uid: id привилегии (default: None)
            name: имя привилегии (default: None)
            link: ссылка привилегии (default: None)

        Returns:
            data: Если удалось получить данные
            None: Если произошла ошибка
        """
        db = await DefaultConnector().connect()
        try:
            async with db.cursor() as cursor:
                if uid and type(uid) == int:
                    await cursor.execute('SELECT * FROM `fd_privillege` WHERE `uid` = %s', (uid,))
                    result = await cursor.fetchone()
                elif name and type(name) == str:
                    await cursor.execute('SELECT * FROM `fd_privillege` WHERE `name` = %s', (name,))
                    result = await cursor.fetchone()
                elif link and type(link) == str:
                    await cursor.execute('SELECT * FROM `fd_privillege` WHERE `link` = %s', (link,))
                    result = await cursor.fetchone()
                else:
                    await cursor.execute('SELECT * FROM `fd_privillege`')
                    result = await cursor.fetchall()
                return result
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except Exception as err:
            log.exception(f'Failed to get privillege (uid: {uid}, name: {name}, link: {link}) to the database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None

    async def remove_privillege(self, uid: int):
        """Удаляет привилегию из базы данных

        Args:
            uid: id привилегии

        Returns:
            True: Если удалось удалить привилегию
            None: Если произошла ошибка
        """
        db = await DefaultConnector().connect()
        try:
            async with db.cursor() as cursor:
                await cursor.execute('DELETE FROM `fd_privillege` WHERE `uid` = %s', (uid, ))
                await db.commit()
                return True
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except Exception as err:
            log.exception(f'Failed to remove privillege to the database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None