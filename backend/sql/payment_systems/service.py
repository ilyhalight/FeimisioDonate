import logging

from sql.db import DefaultConnector
from models.payment_system import PaymentSystem

log = logging.getLogger('server')


class DbPaymentSystemsService:
    def __init__(self) -> None:
        self.database_sc = 'fd_payment_system' # Название таблицы в базе данных (для логов)

    async def init_table(self):
        """Создает таблицу в базе данных для правильной работы"""
        db = await DefaultConnector().connect()
        try:
            async with db.cursor() as cursor:
                await cursor.execute("""CREATE TABLE IF NOT EXISTS `fd_payment_system` (
                    `uid` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                    `name` VARCHAR(255) NOT NULL,
                    `disabled` BOOLEAN DEFAULT FALSE
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

    async def add(self, payment_system: PaymentSystem):
        """Добавляет платежку в базу данных

        Returns:
            True: Если удалось добавить платежку
            None: Если произошла ошибка
        """
        db = await DefaultConnector().connect()
        try:
            async with db.cursor() as cursor:
                await cursor.execute('INSERT INTO `fd_payment_system` (`name`, `disabled`) VALUES (%s, %s)',
                                    (payment_system.name, payment_system.disabled))
                await db.commit()
                return True
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except Exception as err:
            log.exception(f'Failed to add a payment system to the database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None


    async def get(self, disabled: int = None):
        """Возвращает платежку из базы данных

        Args:
            disabled: статус привилегии (default: None)

        Returns:
            data: Если удалось получить данные
            None: Если произошла ошибка
        """
        db = await DefaultConnector().connect()
        try:
            async with db.cursor() as cursor:
                if disabled and type(disabled) == int:
                    await cursor.execute('SELECT * FROM `fd_payment_system` WHERE `disabled` = %s', (disabled, ))
                    result = await cursor.fetchall()
                else:
                    await cursor.execute('SELECT * FROM `fd_payment_system`')
                    result = await cursor.fetchall()
                return result
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except Exception as err:
            log.exception(f'Failed to get payment system from the database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None

    async def remove(self, uid: int):
        """Удаляет платежку из базы данных

        Args:
            uid: id привилегии

        Returns:
            True: Если удалось удалить платежку
            None: Если произошла ошибка
        """
        db = await DefaultConnector().connect()
        try:
            async with db.cursor() as cursor:
                await cursor.execute('DELETE FROM `fd_payment_system` WHERE `uid` = %s', (uid, ))
                await db.commit()
                return True
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except Exception as err:
            log.exception(f'Failed to remove payment system from the database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None