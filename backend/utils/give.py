import time
import uuid

from aiogram.utils.markdown import escape_md

from config.load import load_json
from logger.masslog import MassLog
from utils.converters import SteamConverters
from utils.console.source import add_vip_ingame
from utils.db import find_privilleges_json
from sql.vip_users.controller import VipUsersController
from sql.sb_admins.controller import SBAdminsController

async def giver_csgo(privillege_uid: int, steamlink: str):
    """Добавляет привилегию пользователю на CS:GO сервере
    
        Args:
            privillege_uid (int): UID привилегии
            steamlink (str): Ссылка на профиль Steam
    """
    try:
        steamid = SteamConverters().url_to_steam64(steamlink)
    except Exception as err:
        await MassLog().error(f'Произошла ошибка при конвертации Steam\-ссылки в SteamID\: {err}')
        return False
    try:
        nickname = SteamConverters().url_to_nickname(steamlink)
    except Exception as err:
        await MassLog().error(f'Произошла ошибка при конвертации Steam\-ссылки в Ник\: {err}')
        nickname = 'unnamed'
    privillege = await find_privilleges_json(int(privillege_uid))
    if steamid and privillege and privillege['name']:
        duration = privillege['duration']
        if duration == 0:
            seconds = 0
        else:
            seconds = duration * 3600
        status = await give_on_csgo_server(steamid, nickname, privillege['name'], seconds)
        if status is False:
            account_id = SteamConverters().to_steamID3(steamid)
            if duration == 0:
                expires = 0
            else:
                expires = int(time.time()) + seconds
            db_status = await give_csgo_database(account_id, nickname, privillege['name'], expires)
            await MassLog().log_by_type(db_status['status'], db_status['logs'])
            return db_status
        await MassLog().log_by_type(db_status['status'], db_status['logs']) 
        return status
    await MassLog().error(f'Произошла ошибка при добавлении привилегии на сервере CS\:GO\.\n\nПроверьте правильность введенных данных: {privillege_uid} \(данные о привилегии\: {escape_md(privillege)}\)\, {escape_md(steamlink)} \(steamid\: {escape_md(steamid)}\)')
    return False

async def give_on_csgo_server(steamid: int, name: str, group: str, seconds: int):
    """Добавляет привилегию пользователю, если у пользователя нету привилегии (пользователь должен быть на сервере)
    
        Args:
            steamid (int): SteamID пользователя (STEAM:1...)
            group (str): Название группы
            seconds (int): Время в секундах, на которое выдается привилегия (0 - навсегда)
    """
    servers = load_json('servers.json')
    groups = load_json('groups.json')['csgo']
    for server in servers['csgo']:
        if server['ip'] != '' and server['port'] != '' and server['rcon'] != '':
            status = await add_vip_ingame(server['ip'], server['port'], server['rcon'], steamid, group, seconds)
            if 'успешно добавлен!' in status:
                if seconds == 0:
                    expires = 0
                else:
                    expires = int(time.time()) + seconds
                account_id = SteamConverters().to_steamID3(steamid)
                for g in groups:
                    if g['name'] == group and g['gid'] > 0 and g['srv_group'] != '':
                        password = uuid.uuid4()
                        await SBAdminsController().add(name, steamid, password, g['admin'], name, g['srv_group'], expires) 
                        return {
                            'status': 'success',
                            'logs': f'Привилегия {group} была успешно выдана [игроку](https://steamcommunity.com/profiles/{account_id})\.\nПривилегия действует до {expires}\.',
                            'web': f'Привилегия {group} была успешно выдана.\n\nВаша привилегия действует до {expires}. Ваш пароль для входа в админку: **{password}** (не забудьте его сохранить). Если привилегия не появилась, вам необходимо перезайти на сервер.'
                        }
                return {
                    'status': 'success',
                    'logs': f'Привилегия {group} была успешно выдана [игроку](https://steamcommunity.com/profiles/{account_id})\.\nПривилегия действует до {expires}\.\n\nПривилегия выдана на сервере {escape_md(server["ip"])}\:{server["port"]}',
                    'web': f'Привилегия {group} была успешно выдана.\n\nВаша привилегия действует до {expires}.'
                }
    return False

async def give_csgo_database(account_id: int, name: str, group: str, expires: int):
    """Добавляет привилегию пользователю, если текущая привилегия пользователя ниже новой"""
    account_id = account_id.split('[U:1:')[-1].split(']')[0]
    current = await VipUsersController().get(account_id)
    groups = load_json('groups.json')['csgo']
    if current and len(current) > 0:
        сurrent_group = current['group']
        current_expires = current['expires']
        current_group_level = -1
        group_level = -1
        for g in groups:
            if g['name'] == сurrent_group:
                current_group_level = g['priority']
            if g['name'] == group:
                group_level = g['priority']
        if current_group_level == -1 and group_level == -1:
            return {
                'status': 'error',
                'logs': f'[Пользователь](https://steamcommunity.com/profiles/[U:1:{account_id}]) попытался выдать неизвестную привилегию {escape_md(group)}\!',
                'web': 'Неизвестная привилегия'
            }
        elif current_group_level == -1 and group_level != -1:
            return {
                'status': 'error',
                'logs': f'[Пользователь](https://steamcommunity.com/profiles/[U:1:{account_id}]) имеет уникальную привилегию не указанную в конфиге\!',
                'web': 'Неизвестная привилегия'
            }
        elif current_group_level != -1 and group_level == -1:
            return {
                'status': 'error',
                'logs': f'[Пользователь](https://steamcommunity.com/profiles/[U:1:{account_id}]) пытается получить привилегию, которой нету в конфиге\!',
                'web': 'Неизвестная привилегия'
            }
        elif current_group_level < group_level:
            await VipUsersController().remove(current['account_id'])
        elif current_group_level == group_level and current_expires != 0 and current_expires < expires:
            await VipUsersController().remove(current['account_id'])
        elif current_group_level == group_level and current_expires != 0 and expires == 0:
            await VipUsersController().remove(current['account_id'])
        else:
            return {
                'status': 'error',
                'logs': f'Привилегия {group} не была выдана [игроку](https://steamcommunity.com/profiles/[U:1:{account_id}])\.\nУ игрока уже есть привилегия выше или равная этой\.',
                'web': 'У вас уже есть привилегия выше или равная этой. Если вы всё равно хотите получить эту привилегию - отпишите по контактам внизу страницы.'
            }
    status = await VipUsersController().add(account_id, name, group, expires)
    if expires == 0:
        str_expires = 'навсегда'
    else:
        str_expires = f'до {expires}'
    if status:
        for g in groups:
            if g['name'] == group and g['gid'] > 0 and g['srv_group'] != '':
                password = uuid.uuid4()
                steamid = SteamConverters().to_steamID(g['steamid'])
                await SBAdminsController().add(name, steamid, password, g['admin'], name, g['srv_group'], expires) 
                return {
                    'status': 'success',
                    'logs': f'Привилегия {group} была успешно выдана [игроку](https://steamcommunity.com/profiles/[U:1:{account_id}])\.\nПривилегия действует {str_expires}\.',
                    'web': f'Привилегия {group} была успешно выдана.\n\nВаша привилегия действует {str_expires}. Ваш пароль для входа в админку: **{password}** (не забудьте его сохранить). Если привилегия не появилась, вам необходимо перезайти на сервер.'
                }
        return {
            'status': 'success',
            'logs': f'Привилегия {group} была успешно выдана [игроку](https://steamcommunity.com/profiles/[U:1:{account_id}])\.\nПривилегия действует {str_expires}\.',
            'web': f'Привилегия {group} была успешно выдана.\n\nВаша привилегия действует {str_expires}. Если привилегия не появилась, вам необходимо перезайти на сервер.'
        }
    return {
        'status': 'error',
        'logs': f'Привилегия {group} не была выдана [игроку](https://steamcommunity.com/profiles/[U:1:{account_id}])\.\nВозникла проблема при добавление привилегии в базу данных\.',
        'web': 'Возникла проблема при добавление привилегии в базу данных. Отпишите по контактам внизу страницы.'
    }
