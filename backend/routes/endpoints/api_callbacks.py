import logging
import os
import time
from fastapi import APIRouter, status, Form, Header
from fastapi.responses import JSONResponse
from aiogram.utils.markdown import escape_md

from sql.promocode_uses.service import DbPromocodeUsesService
from logger.masslog import MassLog
from utils.db import find_privilleges_json, find_promocodes_json
from utils.sign import sign
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


@router.post('/freekassa', response_class = JSONResponse, summary = 'Callback for freekassa payments', responses = payment_methods_responses)
async def index(
    MERCHANT_ID: int = Form(), AMOUNT: int = Form(), intid: int = Form(), MERCHANT_ORDER_ID: int|str = Form(),
    P_EMAIL: str = Form(default = None), P_PHONE: str = Form(default = None), CUR_ID: int = Form(), SIGN: str = Form(), us_uid: str = Form(),
    us_price: int = Form(), us_steamLink: str = Form(), us_promoCode: str = Form(default=""), payer_account: str = Form(default = None), commission: int|float|str = Form(),
    HTTP_X_REAL_IP: str = Header(default = None), REMOTE_ADDR: str = Header(default = None)
    ):
    """
    Callback for freekassa payments

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
        server_sign = sign(MERCHANT_ID, AMOUNT, os.environ.get('FREEKASSA_SECRET'), MERCHANT_ORDER_ID)
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
        privilleges = await find_privilleges_json(int(us_uid))
        if privilleges:
            if us_steamLink.startswith('id'):
                us_steamLink_arr = us_steamLink.split('id', maxsplit = 1)
                part = 'id/'
            elif us_steamLink.startswith('profiles'):
                us_steamLink_arr = us_steamLink.split('profiles', maxsplit = 1)
                part = 'profiles/'
            else:
                part = ''
            if part and len(us_steamLink_arr) > 1:
                steam_link = f'https://steamcommunity.com/{part}/{us_steamLink_arr[1]}'
            else:
                steam_link = us_steamLink
            await MassLog().success(f'[Пользователь]({steam_link}) оплатил привилегию **{escape_md(privilleges["name"])}** \({us_uid}\) за **{escape_md(AMOUNT)}** руб\. \(комиссия: **{escape_md(commission)}**\) через FreeKassa \(Метод: **{escape_md(currency)}**\ \| Промокод: **{escape_md(us_promoCode)}**\)')
            res = await giver_csgo(us_uid, steam_link)
            steamid64 = SteamConverters().url_to_steam64(steam_link)
            steamid = SteamConverters().to_steamID(steamid64)
            promocode = await find_promocodes_json(us_promoCode)
            if us_promoCode != '' and len(promocode) > 0:
                try:
                    await DbPromocodeUsesService().add(us_promoCode, steamid, us_uid, time.time())
                    log.info(f'Added promocode {us_promoCode} usages to Database')
                except Exception:
                    await MassLog().success(f'Произошла ошибка при добавление использования промокода {escape_md(us_promoCode)} в Базу Данных\. \([Пользователь]({steam_link})**, привилегия: {escape_md(privilleges["name"])}** \({us_uid}\), цена: **{escape_md(AMOUNT)}** руб\. \(комиссия: **{escape_md(commission)}**) через FreeKassa \(Метод: **{escape_md(currency)}**\)')
                    log.exception('Error while adding usage to promo')
            if res:
                return JSONResponse(content = {'auth': 'OK', 'status': res['status'], 'message': res['web']}, status_code = status.HTTP_200_OK)
            else:
                return JSONResponse(content = {'auth': 'OK', 'status': 'error', 'message': 'Не удалось выдать привилегию'}, status_code = status.HTTP_200_OK)
        log.debug('privilleges is wrong')
        return JSONResponse(content = {'error': 'unknown privillege uid'}, status_code = status.HTTP_400_BAD_REQUEST)
    return JSONResponse(content = {'error': 'Request from not availabled IP or MERCHANT_ID is wrong'}, status_code = status.HTTP_403_FORBIDDEN)