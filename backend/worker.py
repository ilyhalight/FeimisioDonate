import logging

from fastapi_utils.tasks import repeat_every

from core.app import app
from sql.privillege.controller import DbPrivillegeController
from sql.privillege_info.controller import DbPrivillegeInfoController
from sql.promocode_uses.controller import DbPromocodeUsesController
from sql.promocodes.controller import DbPromocodesController
from utils.db import save_privilleges_to_json, save_privilleges_info_to_json, save_promocodes_to_json


log = logging.getLogger('worker')

def init_worker():
    @app.on_event('startup')
    async def startup():
        log.info('Worker started')
        await DbPrivillegeController().init()
        await DbPrivillegeInfoController().init()
        await DbPromocodesController().init()
        await DbPromocodeUsesController().init()
        log.info('DB initialized')

    @app.on_event("startup")
    @repeat_every(seconds = 60 * 5)  # 5 min
    async def worker():
        await save_privilleges_to_json()
        await save_privilleges_info_to_json()
        await save_promocodes_to_json()
