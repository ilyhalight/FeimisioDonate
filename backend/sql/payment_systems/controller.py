from sql.payment_systems.service import DbPaymentSystemsService
from models.payment_system import PaymentSystem

class DbPaymentSystemsController:
    async def init(self):
        """Создаёт таблицу в базе данных, если она не существует"""
        return await DbPaymentSystemsService().init_table()

    async def add_payment_system(self, payment_system: PaymentSystem):
        """Добавляет платежку в базу данных"""
        return await DbPaymentSystemsService().add(payment_system)

    async def get_all(self):
        """Возвращает все платежки из базы данных"""
        return await DbPaymentSystemsService().get()

    async def get_by_status(self, disabled: int):
        """Возвращает платежку из базы данных по статусу"""
        return await DbPaymentSystemsService().get(disabled)

    async def remove(self, uid: int):
        """Удаляет платежку из базы данных"""
        return await DbPaymentSystemsService().remove(uid)