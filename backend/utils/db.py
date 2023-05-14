import json
import aiofiles
import logging

from sql.privilege.controller import DbPrivilegeController
from sql.privilege_info.controller import DbPrivilegeInfoController
from sql.promocodes.controller import DbPromocodesController
from sql.payment_systems.controller import DbPaymentSystemsController

log = logging.getLogger('worker')


async def save_privileges_to_json():
    """Сохраняет доступные привилегии из базы данных в json файл"""
    privileges = await DbPrivilegeController().get_all()
    if privileges:
        async with aiofiles.open('config/privileges.json', 'w', encoding = 'utf-8') as f:
            await f.write(json.dumps(privileges, indent=4))
            log.info('privileges saved to json')
            await f.close()

async def get_privileges_json():
    """Возвращает доступные привилегии из json файла"""
    try:
        async with aiofiles.open('config/privileges.json', 'r', encoding = 'utf-8') as f:
            privileges = await f.read()
            return json.loads(privileges)
    except FileNotFoundError:
        return []

async def find_privileges_json(uid: int):
    """Возвращает информацию о привилегии из json файла по uid"""
    privileges = await get_privileges_json()
    if privileges:
        for privilege in privileges:
            if privilege['uid'] == uid:
                return privilege
    return []

async def save_privileges_info_to_json():
    """Сохраняет информацию о привилегии из базы данных в json файл"""
    privileges = await DbPrivilegeInfoController().get_all()
    if privileges:
        async with aiofiles.open('config/privileges_info.json', 'w', encoding = 'utf-8') as f:
            await f.write(json.dumps(privileges, indent=4))
            log.info('privileges info saved to json')
            await f.close()

async def get_privileges_info_json():
    """Возвращает информацию о привилегии из json файла"""
    try:
        async with aiofiles.open('config/privileges_info.json', 'r', encoding = 'utf-8') as f:
            privileges = await f.read()
            return json.loads(privileges)
    except FileNotFoundError:
        return []

async def find_privileges_info_json(link: str):
    """Возвращает информацию о привилегии из json файла по названию привилегии (link)"""
    privileges = await get_privileges_info_json()
    res = []
    if privileges:
        for privilege in privileges:
            if privilege['link'] == link:
                res.append(privilege)
    return res

async def save_promocodes_to_json():
    """Сохраняет доступные промокоды из базы данных в json файл"""
    promocodes = await DbPromocodesController().get_all()
    if promocodes:
        async with aiofiles.open('config/promocodes.json', 'w', encoding = 'utf-8') as f:
            await f.write(json.dumps(promocodes, indent=4))
            log.info('promocodes saved to json')
            await f.close()

async def save_payment_systems_to_json():
    """Сохраняет доступные платежки из базы данных в json файл"""
    payment_systems = await DbPaymentSystemsController().get_all()
    if payment_systems:
        async with aiofiles.open('config/payment_systems.json', 'w', encoding = 'utf-8') as f:
            await f.write(json.dumps(payment_systems, indent=4))
            log.info('payment systems saved to json')
            await f.close()

async def get_payment_systems_json():
    """Возвращает доступные платежки из json файла"""
    try:
        async with aiofiles.open('config/payment_systems.json', 'r', encoding = 'utf-8') as f:
            payment_systems = await f.read()
            return json.loads(payment_systems)
    except FileNotFoundError:
        return []

async def get_promocodes_json():
    """Возвращает доступные промокоды из json файла"""
    try:
        async with aiofiles.open('config/promocodes.json', 'r', encoding = 'utf-8') as f:
            promocodes = await f.read()
            return json.loads(promocodes)
    except FileNotFoundError:
        return []

async def find_promocodes_json(key: str):
    """Возвращает информацию о проомокоде из json файла по uid"""
    promocodes = await get_promocodes_json()
    if promocodes:
        for promocode in promocodes:
            if promocode['key'] == key:
                return promocode
    return []