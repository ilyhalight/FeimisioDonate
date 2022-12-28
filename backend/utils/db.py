import json
import aiofiles
import logging

from sql.privillege.controller import DbPrivillegeController
from sql.privillege_info.controller import DbPrivillegeInfoController

log = logging.getLogger('worker')


async def save_privilleges_to_json():
    """Сохраняет доступные привилегии из базы данных в json файл"""
    privilleges = await DbPrivillegeController().get_all()
    async with aiofiles.open('config/privilleges.json', 'w', encoding = 'utf-8') as f:
        await f.write(json.dumps(privilleges))
        await f.close()

async def get_privilleges_json():
    """Возвращает доступные привилегии из json файла"""
    try:
        async with aiofiles.open('config/privilleges.json', 'r', encoding = 'utf-8') as f:
            privilleges = await f.read()
            return json.loads(privilleges)
    except FileNotFoundError:
        return []

async def find_privilleges_json(uid: int):
    """Возвращает информацию о привилегии из json файла по uid"""
    privilleges = await get_privilleges_json()
    if privilleges:
        for privillege in privilleges:
            if privillege['uid'] == uid:
                return privillege
    return []

async def save_privilleges_info_to_json():
    """Сохраняет информацию о привилегии из базы данных в json файл"""
    privilleges = await DbPrivillegeInfoController().get_all()
    async with aiofiles.open('config/privilleges_info.json', 'w', encoding = 'utf-8') as f:
        await f.write(json.dumps(privilleges))
        await f.close()

async def get_privilleges_info_json():
    """Возвращает информацию о привилегии из json файла"""
    try:
        async with aiofiles.open('config/privilleges_info.json', 'r', encoding = 'utf-8') as f:
            privilleges = await f.read()
            return json.loads(privilleges)
    except FileNotFoundError:
        return []

async def find_privilleges_info_json(link: str):
    """Возвращает информацию о привилегии из json файла по названию привилегии (link)"""
    privilleges = await get_privilleges_info_json()
    res = []
    if privilleges:
        for privillege in privilleges:
            if privillege['link'] == link:
                res.append(privillege)
    return res
