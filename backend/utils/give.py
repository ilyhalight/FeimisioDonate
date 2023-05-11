import time
import uuid
import logging

from aiogram.utils.markdown import escape_md
from fastapi import status
from fastapi.responses import JSONResponse, RedirectResponse
from datetime import datetime

from config.load import load_json
from logger.masslog import MassLog
from utils.converters import SteamConverters
from utils.console.source import add_vip_ingame
from utils.price import get_final_price
from utils.db import find_privileges_json, find_promocodes_json
from sql.vip_users.controller import VipUsersController
from sql.sb_admins.controller import SBAdminsController
from sql.promocode_uses.controller import DbPromocodeUsesController

log = logging.getLogger('server')

async def give_privilege_callback(aggregator: str, p_uid: int, p_steam_link: str, amount: int, commission: str, method: str, p_promo_code: str):
    """Общая функция для выдачи привилегий

    Args:
        aggregator (str): платежный агрегатор
        p_uid (int): uid привилегии
        p_steam_link (str): необработанная часть стим ссылки (пример: idToilOfficial)
        amount (int): сумма платежа
        commission (str): комиссия
        method (str): метод платежа
        p_promo_code (str): промокод
    """
    privileges = await find_privileges_json(int(p_uid))
    if privileges:
        if p_steam_link.startswith('id'):
            us_steamLink_arr = p_steam_link.split('id', maxsplit = 1)
            part = 'id/'
        elif p_steam_link.startswith('profiles'):
            us_steamLink_arr = p_steam_link.split('profiles', maxsplit = 1)
            part = 'profiles/'
        else:
            part = ''
        if part and len(us_steamLink_arr) > 1:
            steam_link = f'https://steamcommunity.com/{part}/{us_steamLink_arr[1]}'
        else:
            steam_link = p_steam_link
        
        price_privilege = await get_final_price(privileges['price'], privileges['discount'], p_promo_code)
        nickname = 'Пользователь'
        try:
            nickname = SteamConverters().url_to_nickname(steam_link)
        except Exception as err:
            log.error(f'Failed get username from Steam: {err}')
        if int(price_privilege) != int(amount):
            await MassLog().error(f'[{escape_md(nickname)}]({steam_link}) оплатил привилегию **{escape_md(privileges["name"])}** \(UID: **{p_uid}**\) за **{escape_md(amount)}** руб\. \(комиссия: **{escape_md(commission)}**\, настоящая цена: **{escape_md(price_privilege)}**\) через **{escape_md(aggregator)}** \(Метод: **{escape_md(method)}** \| Промокод: **{escape_md(p_promo_code)}**\)\n\n**ОШИБКА:** Не совпадает сумма платежа и цена привилегии!!!')
            return JSONResponse(content = {'auth': 'OK', 'status': 'error', 'message': 'Не совпадает сумма платежа и цена привилегии!'}, status_code = status.HTTP_402_PAYMENT_REQUIRED)

        if int(amount) != 0:
            await MassLog().success(f'[{escape_md(nickname)}]({steam_link}) оплатил привилегию **{escape_md(privileges["name"])}** \(UID: **{p_uid}**\) за **{escape_md(amount)}** руб\. \(комиссия: **{escape_md(commission)}**\) через **{escape_md(aggregator)}** \(Метод: **{escape_md(method)}** \| Промокод: **{escape_md(p_promo_code)}**\)')
        else:
            await MassLog().info(f'[{escape_md(nickname)}]({steam_link}) запросил бесплатную привилегию {escape_md(privileges["name"])} \(промокод: {escape_md(p_promo_code)}\)')
        res = await giver_csgo(p_uid, steam_link)
        steamid64 = SteamConverters().url_to_steam64(steam_link)
        steamid = SteamConverters().to_steamID(steamid64)
        promocode = await find_promocodes_json(p_promo_code)
        if p_promo_code != '' and len(promocode) > 0:
            try:
                await DbPromocodeUsesController().add(p_promo_code, steamid, p_uid, int(time.time()))
                log.info(f'Added promocode {p_promo_code} usages to Database')
            except Exception:
                await MassLog().success(f'Произошла ошибка при добавление использования промокода {escape_md(p_promo_code)} в Базу Данных\. \([{escape_md(nickname)}]({steam_link})**, привилегия: {escape_md(privileges["name"])}** \({p_uid}\), цена: **{escape_md(amount)}** руб\. \(комиссия: **{escape_md(commission)}**) через **{escape_md(aggregator)}** \(Метод: **{escape_md(method)}**\)')
                log.exception('Error while adding usage to promo')
        if res:
            if amount != 0:
                return JSONResponse(content = {'auth': 'OK', 'status': res['status'], 'message': res['web']}, status_code = status.HTTP_200_OK)
            else:
                return RedirectResponse(url = f'/results/success', status_code = status.HTTP_303_SEE_OTHER)
        else:
            return JSONResponse(content = {'auth': 'OK', 'status': 'error', 'message': 'Не удалось выдать привилегию'}, status_code = status.HTTP_200_OK)
    log.debug('privileges is wrong')
    return JSONResponse(content = {'error': 'unknown privilege uid'}, status_code = status.HTTP_400_BAD_REQUEST)


async def giver_csgo(privilege_uid: int, steamlink: str):
    """Добавляет привилегию пользователю на CS:GO сервере
    
        Args:
            privilege_uid (int): UID привилегии
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
    privilege = await find_privileges_json(int(privilege_uid))
    if steamid and privilege and privilege['name']:
        duration = privilege['duration']
        if duration == 0:
            seconds = 0
        else:
            seconds = duration * 3600
        status = await give_on_csgo_server(steamid, nickname, privilege['name'], seconds)
        if status is False:
            account_id = SteamConverters().to_steamID3(steamid)
            if duration == 0:
                expires = 0
            else:
                expires = int(time.time()) + seconds
            db_status = await give_csgo_database(account_id, nickname, privilege['name'], expires)
            await MassLog().log_by_type(db_status['status'], db_status['logs'])
            return db_status
        await MassLog().log_by_type(db_status['status'], db_status['logs']) 
        return status
    await MassLog().error(f'Произошла ошибка при добавлении привилегии на сервере CS\:GO\.\n\nПроверьте правильность введенных данных: {privilege_uid} \(данные о привилегии\: {escape_md(privilege)}\)\, {escape_md(steamlink)} \(steamid\: {escape_md(steamid)}\)')
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
                    date = 'навсегда'
                else:
                    expires = int(time.time()) + seconds
                    date = datetime.fromtimestamp(expires).strftime('%d.%m.%Y %H:%M')
                account_id = SteamConverters().to_steamID3(steamid)
                nickname = 'Пользователь'
                steam_link = f'https://steamcommunity.com/profiles/{account_id}'
                try:
                    nickname = SteamConverters().url_to_nickname(steam_link)
                except Exception as err:
                    log.error(f'Failed get username from Steam: {err}')
                for g in groups:
                    if g['name'] == group and g['gid'] > 0 and g['srv_group'] != '':
                        password = uuid.uuid4()
                        await SBAdminsController().add(name, steamid, password, g['admin'], name, g['srv_group'], expires) 
                        return {
                            'status': 'success',
                            'logs': f'Привилегия {escape_md(group)} была успешно выдана [{escape_md(nickname)}]({steam_link})\.\nПривилегия действует до **{escape_md(date)}**\.',
                            'web': f'Привилегия {group} была успешно выдана\n\nВаша привилегия действует до {escape_md(date)}. Ваш пароль для входа в админку: **{password}** (не забудьте его сохранить). Если привилегия не появилась, вам необходимо перезайти на сервер.'
                        }
                return {
                    'status': 'success',
                    'logs': f'Привилегия {escape_md(group)} была успешно выдана [{escape_md(nickname)}]({steam_link})\.\nПривилегия действует до **{escape_md(date)}**\.\n\nПривилегия выдана на сервере {escape_md(server["ip"])}\:{server["port"]}',
                    'web': f'Привилегия {group} была успешно выдана.\n\nВаша привилегия действует до {escape_md(date)}.'
                }
    return False

async def give_csgo_database(account_id: int, name: str, group: str, expires: int):
    """Добавляет привилегию пользователю, если текущая привилегия пользователя ниже новой"""
    account_id = account_id.split('[U:1:')[-1].split(']')[0]
    current = await VipUsersController().get(account_id)
    groups = load_json('groups.json')['csgo']

    nickname = 'Пользователь'
    steam_link = f'https://steamcommunity.com/profiles/[U:1:{account_id}]'
    try:
        nickname = SteamConverters().url_to_nickname(steam_link)
    except Exception as err:
        log.error(f'Failed get username from Steam: {err}')
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
                'logs': f'[{escape_md(nickname)}]({steam_link}) попытался выдать неизвестную привилегию {escape_md(group)}\!',
                'web': 'Неизвестная привилегия'
            }
        elif current_group_level == -1 and group_level != -1:
            return {
                'status': 'error',
                'logs': f'[{escape_md(nickname)}]({steam_link}) имеет уникальную привилегию не указанную в конфиге\!',
                'web': 'Неизвестная привилегия'
            }
        elif current_group_level != -1 and group_level == -1:
            return {
                'status': 'error',
                'logs': f'[{escape_md(nickname)}]({steam_link}) пытается получить привилегию, которой нету в конфиге\!',
                'web': 'Неизвестная привилегия'
            }
        elif current_group_level < group_level:
            await VipUsersController().remove(current['account_id'])
            await MassLog().info(f'Привилегия **{escape_md(сurrent_group)}** была удалена у [{escape_md(nickname)}]({steam_link}) для выдачи новой привилегии с более высоким приоритетом\.')
        elif current_group_level == group_level and current_expires != 0 and current_expires < expires:
            await VipUsersController().remove(current['account_id'])
            await MassLog().info(f'Привилегия **{escape_md(group)}** была удалена у [{escape_md(nickname)}]({steam_link}) для выдачи новой привилегии с более длинным сроком действия\.')
        elif current_group_level == group_level and current_expires != 0 and expires == 0:
            await VipUsersController().remove(current['account_id'])
            await MassLog().info(f'Привилегия **{escape_md(group)}** была удалена у [{escape_md(nickname)}]({steam_link}) для выдачи новой привилегии с бесконечным сроком действия\.')
        else:
            return {
                'status': 'error',
                'logs': f'Привилегия **{escape_md(group)}** не была выдана [{escape_md(nickname)}]({steam_link})\.\nУ игрока уже есть привилегия выше или равная этой\.',
                'web': 'У вас уже есть привилегия выше или равная этой. Если вы всё равно хотите получить эту привилегию - отпишите по контактам внизу страницы.'
            }
    status = await VipUsersController().add(account_id, name, group, expires)
    if expires == 0:
        str_expires = 'навсегда'
    else:
        str_expires = escape_md(f'до {datetime.fromtimestamp(expires).strftime("%d.%m.%Y %H:%M")}')
    if status:
        for g in groups:
            if g['name'] == group and g['gid'] > 0 and g['srv_group'] != '':
                password = uuid.uuid4()
                steamid = SteamConverters().to_steamID(f'[U:1:{account_id}]')
                await SBAdminsController().add(name, steamid, password, g['gid'], name, g['srv_group'], expires) 
                return {
                    'status': 'success',
                    'logs': f'Привилегия **{escape_md(group)}** была успешно выдана [{escape_md(nickname)}]({steam_link})\.\nПривилегия действует **{str_expires}**\.',
                    'web': f'Привилегия {group} была успешно выдана.\n\nВаша привилегия действует {str_expires}. Ваш пароль для входа в админку: **{password}** (не забудьте его сохранить). Если привилегия не появилась, вам необходимо перезайти на сервер.'
                }
        return {
            'status': 'success',
            'logs': f'Привилегия **{escape_md(group)}** была успешно выдана [{escape_md(nickname)}]({steam_link})\.\nПривилегия действует **{str_expires}**\.',
            'web': f'Привилегия {group} была успешно выдана.\n\nВаша привилегия действует {str_expires}. Если привилегия не появилась, вам необходимо перезайти на сервер.'
        }
    return {
        'status': 'error',
        'logs': f'Привилегия **{escape_md(group)}** не была выдана [{escape_md(nickname)}]({steam_link})\.\nВозникла проблема при добавление привилегии в базу данных\.',
        'web': 'Возникла проблема при добавление привилегии в базу данных. Отпишите по контактам внизу страницы.'
    }
