import logging
import os
import time
import aiohttp
from fastapi import APIRouter, status, Form, Header
from fastapi.responses import JSONResponse
from aiogram.utils.markdown import escape_md

from sql.promocode_uses.service import DbPromocodeUsesService
from logger.masslog import MassLog
from utils.db import find_privilleges_json, find_promocodes_json
from utils.sign import sign_md5, sign_sha1
from utils.give import giver_csgo
from utils.converters import SteamConverters

router = APIRouter()
log = logging.getLogger('server')

payment_methods_responses = {
    303: {'description': 'Redirected to another page'},
    404: {'description': 'Not found aggregator'},
}

currencies = {
    '1': 	'FK WALLET RUB',
    '2': 	'FK WALLET USD',
    '3':	'FK WALLET EUR',
    '4': 	'VISA RUB',
    '6':	'Yoomoney',
    '7':	'VISA UAH',
    '8':	'MasterCard RUB',
    '9':	'MasterCard UAH',
    '10':	'Qiwi',
    '11':	'VISA EUR',
    '12':	'МИР',
    '13':	'Онлайн банк',
    '14':	'USDT (ERC20)',
    '15':	'USDT (TRC20)',
    '16':	'Bitcoin Cash',
    '17':	'BNB',
    '18':	'DASH',
    '19':	'Dogecoin',
    '20':	'ZCash',
    '21':	'Monero',
    '22':	'Waves',
    '23':	'Ripple',
    '24':	'Bitcoin',
    '25':	'Litecoin',
    '26':	'Ethereum',
    '27':	'SteamPay',
    '28':	'Мегафон',
    '32':	'VISA USD',
    '33':	'Perfect Money USD',
    '34':	'Shiba Inu',
    '35':	'QIWI API',
    '36':	'Card RUB API',
    '37':	'Google pay',
    '38':	'Apple pay',
    '39':	'Tron',
    '40':	'Webmoney WMZ',
    '41':	'VISA / MasterCard KZT',
    '42':	'СБП'
}

async def give_privillege_callback(aggregator: str, p_uid: int, p_steam_link: str, amount: int, commission: str, method: str, p_promo_code: str):
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
    privilleges = await find_privilleges_json(int(p_uid))
    if privilleges:
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
        await MassLog().success(f'[Пользователь]({steam_link}) оплатил привилегию **{escape_md(privilleges["name"])}** \({p_uid}\) за **{escape_md(amount)}** руб\. \(комиссия: **{escape_md(commission)}**\) через {escape_md(aggregator)} \(Метод: **{escape_md(method)}** \| Промокод: **{escape_md(p_promo_code)}**\)')
        res = await giver_csgo(p_uid, steam_link)
        steamid64 = SteamConverters().url_to_steam64(steam_link)
        steamid = SteamConverters().to_steamID(steamid64)
        promocode = await find_promocodes_json(p_promo_code)
        if p_promo_code != '' and len(promocode) > 0:
            try:
                await DbPromocodeUsesService().add(p_promo_code, steamid, p_uid, time.time())
                log.info(f'Added promocode {p_promo_code} usages to Database')
            except Exception:
                await MassLog().success(f'Произошла ошибка при добавление использования промокода {escape_md(p_promo_code)} в Базу Данных\. \([Пользователь]({steam_link})**, привилегия: {escape_md(privilleges["name"])}** \({p_uid}\), цена: **{escape_md(amount)}** руб\. \(комиссия: **{escape_md(commission)}**) через {escape_md(aggregator)} \(Метод: **{escape_md(method)}**\)')
                log.exception('Error while adding usage to promo')
        if res:
            return JSONResponse(content = {'auth': 'OK', 'status': res['status'], 'message': res['web']}, status_code = status.HTTP_200_OK)
        else:
            return JSONResponse(content = {'auth': 'OK', 'status': 'error', 'message': 'Не удалось выдать привилегию'}, status_code = status.HTTP_200_OK)
    log.debug('privilleges is wrong')
    return JSONResponse(content = {'error': 'unknown privillege uid'}, status_code = status.HTTP_400_BAD_REQUEST)


@router.post('/freekassa', response_class = JSONResponse, summary = 'Callback for freekassa payments', responses = payment_methods_responses)
async def index(
    MERCHANT_ID: int = Form(), AMOUNT: int = Form(), intid: int = Form(), MERCHANT_ORDER_ID: int|str = Form(),
    P_EMAIL: str = Form(default = None), P_PHONE: str = Form(default = None), CUR_ID: int = Form(), SIGN: str = Form(), us_uid: str = Form(),
    us_price: int = Form(), us_steamLink: str = Form(), us_promoCode: str = Form(default=""), payer_account: str = Form(default = None), commission: int|float|str = Form(),
    HTTP_X_REAL_IP: str = Header(default = None), REMOTE_ADDR: str = Header(default = None)
    ):
    """Callback for freekassa payments

    Args:
        MERCHANT_ID 	ID Вашего магазина
        AMOUNT 	Сумма платежа
        intid 	Номер операции Free-Kassa
        MERCHANT_ORDER_ID 	Ваш номер заказа
        P_EMAIL 	Email плательщика
        P_PHONE 	Телефон плательщика (если указан)
        CUR_ID 	ID электронной валюты, который был оплачен заказ список валют
        SIGN 	Подпись запроса методика формирования подписи в данных оповещения
        payer_account 	Номер счета/карты плательщика
        commission 	Сумма комиссии в валюте платежа
        us_uid: UID пользователя
        us_price: Цена привилегии
        us_steamLink: Ссылка на профиль Steam
        us_promoCode: Промокод
    Args (Headers):
        HTTP_X_REAL_IP 	IP адрес
        REMOTE_ADDR 	IP адрес

    """
    log.info(f'Callback for freekassa payments: {locals()}')
    if str(MERCHANT_ID) == os.environ.get('FREEKASSA_SHOPID'):
        log.debug('IP is valid')
        server_sign = sign_md5(MERCHANT_ID, AMOUNT, os.environ.get('FREEKASSA_SECRET'), MERCHANT_ORDER_ID)
        if server_sign != SIGN:
            return JSONResponse(content = {'error': 'Wrong SIGN'}, status_code = status.HTTP_403_FORBIDDEN)
        log.debug('SIGN is valid')
        if str(AMOUNT) != str(us_price):
            return JSONResponse(content = {'error': 'Incorrect payment amount'}, status_code = status.HTTP_403_FORBIDDEN)
        log.debug('AMOUNT is valid')
        if str(CUR_ID) in currencies:
            currency = currencies[str(CUR_ID)]
        else:
            currency = 'Unknown'
        return await give_privillege_callback('FreeKassa', us_uid, us_steamLink, AMOUNT, commission, currency, us_promoCode)
    return JSONResponse(content = {'error': 'Request from not availabled IP or MERCHANT_ID is wrong'}, status_code = status.HTTP_403_FORBIDDEN)

@router.get('/crystalpay', summary = 'Callback for crystalpay payments')
async def index(ID: str, AMOUNT: int, PAYAMOUNT: float, PAYMETHOD: str, CURRENCY: str, HASH: str, EXTRA: str):
    """Callback for crystalpay payments

    Args:
        ID (str): ID платежа
        AMOUNT (int): Изначальная сумма платежа
        PAYAMOUNT (float): Сумма, которую заплатил клиент
        PAYMETHOD (str): Метод - btc, lztm, eth
        CURRENCY (str): Валюта - BITCOIN, LZTMARKET, ETHEREUM
        HASH (str): Хэш операции для проверки
        EXTRA (str): Комментарий, указанный при оплате
    """
    if ID and CURRENCY and HASH:
        server_sign = sign_sha1(ID, CURRENCY, os.environ.get('CRYSTALPAY_SECRET2'))
        if server_sign != HASH:
            log.debug('wrong hash')
            return JSONResponse(content = {'error': 'Wrong HASH'}, status_code = status.HTTP_403_FORBIDDEN)
        log.debug('SIGN is valid')
        p_uid = EXTRA.split(',')[0]
        p_amount = EXTRA.split(',')[1]
        if str(AMOUNT) != str(p_amount):
            log.debug('wrong amount')
            return JSONResponse(content = {'error': 'Incorrect payment amount'}, status_code = status.HTTP_403_FORBIDDEN)
        p_steam_link = EXTRA.split(',')[2]
        log.debug(EXTRA)
        p_promo_code = EXTRA.split(',')[3]
        log.debug(p_promo_code)
        commission = PAYAMOUNT - AMOUNT

        crystalpay_shopid = os.environ.get('CRYSTALPAY_SHOPID')
        crystalpay_secret = os.environ.get('CRYSTALPAY_SECRET')
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.crystalpay.ru/v1/', params = {
                'o': 'invoice-check',
                'n': crystalpay_shopid,
                's': crystalpay_secret,
                'i': ID
            }) as resp:
                data = await resp.json()
                log.debug(data)
                if data['state'] == 'payed':
                    return await give_privillege_callback('CrystalPay', p_uid, p_steam_link, AMOUNT, commission, PAYMETHOD, p_promo_code)
                else:
                    return JSONResponse(content = {'error': 'Privilege has not yet been paid'}, status_code = status.HTTP_402_PAYMENT_REQUIRED)
    log.debug('request is wrong')
    return JSONResponse(content = {'error': 'Request is wrong'}, status_code = status.HTTP_403_FORBIDDEN)
