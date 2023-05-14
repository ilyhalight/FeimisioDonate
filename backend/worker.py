import logging

from fastapi_utils.tasks import repeat_every

from core.app import app
from sql.privilege.controller import DbPrivilegeController
from sql.privilege_info.controller import DbPrivilegeInfoController
from sql.promocode_uses.controller import DbPromocodeUsesController
from sql.promocodes.controller import DbPromocodesController
from sql.payment_systems.controller import DbPaymentSystemsController
from utils.db import save_privileges_to_json, save_privileges_info_to_json, save_promocodes_to_json, save_payment_systems_to_json


log = logging.getLogger('worker')

def init_worker():
    @app.on_event('startup')
    async def startup():
        log.info('Worker started')
        await DbPrivilegeController().init()
        await DbPrivilegeInfoController().init()
        await DbPromocodesController().init()
        await DbPromocodeUsesController().init()
        await DbPaymentSystemsController().init()
        log.info('DB initialized')

    @app.on_event("startup")
    @repeat_every(seconds = 60 * 2)  # 2 min
    async def worker():
        log.info('Recache worker started')
        await save_privileges_to_json()
        await save_privileges_info_to_json()
        await save_promocodes_to_json()
        await save_payment_systems_to_json()
        log.info('Recache worker finished')
