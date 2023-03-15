import logging

from sql.db import DefaultConnector

log = logging.getLogger('server')


class DbPrivilegeInfoService:
    def __init__(self) -> None:
        self.database_sc = 'fd_privilege_info' # Название таблицы в базе данных (для логов)

    async def init_table(self):
        """Создает таблицу в базе данных для правильной работы"""
        db = await DefaultConnector().connect()
        try:
            async with db.cursor() as cursor:
                await cursor.execute("""CREATE TABLE IF NOT EXISTS `fd_privilege_info` (
                    `uid` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                    `link` VARCHAR(255) NOT NULL,
                    `name` VARCHAR(255) NOT NULL,
                    `desc` VARCHAR(255) NOT NULL,
                    `img_link` VARCHAR(255) DEFAULT NULL,
                    `is_big_img` BOOLEAN DEFAULT FALSE,
                    `img_reverse_side` BOOLEAN DEFAULT FALSE
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

    async def add(self, link: str, name: str, desc: str, img_link: str = None, is_big_img: bool = None, img_reverse_side: bool = None):
        """Добавляет привилегию в базу данных

        Args:
            link: имя привилегии (ссылки)
            name: имя блока
            desc: описание блока
            img_link: ссылка на картинку (default None)
            is_big_img: это большая картинка? (default False, если img_link не указан, то None)
            img_reverse_side: это развернутый блок картинки? (default False, если img_link не указан, то None)

        Returns:
            True: Если удалось добавить информацию о привилегии
            None: Если произошла ошибка
        """
        db = await DefaultConnector().connect()
        try:
            async with db.cursor() as cursor:
                if img_link:
                    is_big_img = False if is_big_img is None else is_big_img
                    img_reverse_side = False if img_reverse_side is None else img_reverse_side
                await cursor.execute('INSERT INTO `fd_privilege_info` (`link`, `name`, `desc`, `img_link`, `is_big_img`, `img_reverse_side` VALUES (%s)', (link, name, desc, img_link, is_big_img, img_reverse_side))
                await db.commit()
                return True
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except Exception as err:
            log.exception(f'Failed to add a privilege information to the database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None

    async def get(self, link: str = None):
        """Возвращает информацию о привилегии из базы данных

        Args:
            link: ссылка привилегии (default: None)

        Returns:
            True: Если удалось получить информацию
            None: Если произошла ошибка
        """
        db = await DefaultConnector().connect()
        try:
            async with db.cursor() as cursor:
                if link and type(link) == str:
                    await cursor.execute('SELECT * FROM `fd_privilege_info` WHERE `link` = %s ORDER BY is_big_img', (link))
                    result = await cursor.fetchall()
                else:
                    await cursor.execute('SELECT * FROM `fd_privilege_info` ORDER BY is_big_img')
                    result = await cursor.fetchall()
                return result
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except Exception as err:
            log.exception(f'Failed to get privilege info (link: {link}) to the database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None

    async def remove(self, uid: int):
        """Удаляет информацию о привилегии из базы данных

        Args:
            uid: id привилегии

        Returns:
            True: Если удалось удалить информацию о привилегию
            None: Если произошла ошибка
        """
        db = await DefaultConnector().connect()
        try:
            async with db.cursor() as cursor:
                await cursor.execute('DELETE FROM `fd_privilege_info` WHERE `uid` = %s', (uid, ))
                await db.commit()
                return True
        except AttributeError as err:
            log.error(f'Failed connection to database: {err}')
            return None
        except Exception as err:
            log.exception(f'Failed to remove privilege information to the database ({self.database_sc}): {err}')
            return None
        finally:
            db.close() if db else None