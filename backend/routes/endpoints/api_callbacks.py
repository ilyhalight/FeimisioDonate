import logging
import os
from fastapi import APIRouter, Request, status, Form, Header
from fastapi.responses import JSONResponse

from models.crystalpay_request import CrystalPayRequest
from utils.give import give_privilege_callback
from utils.sign import sign_md5, sign_sha1, sign_hmac_sha256, sign_md5_upper
from utils.utils import sort_dict

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
    if str(MERCHANT_ID) == os.environ.get('FREEKASSA_SHOPID'):
        server_sign = sign_md5(MERCHANT_ID, AMOUNT, os.environ.get('FREEKASSA_SECRET'), MERCHANT_ORDER_ID)
        if server_sign != SIGN:
            return JSONResponse(content = {'error': 'Wrong SIGN'}, status_code = status.HTTP_403_FORBIDDEN)
        if str(AMOUNT) != str(us_price):
            return JSONResponse(content = {'error': 'Incorrect payment amount'}, status_code = status.HTTP_403_FORBIDDEN)
        if str(CUR_ID) in currencies:
            currency = currencies[str(CUR_ID)]
        else:
            currency = 'Unknown'
        return await give_privilege_callback('FreeKassa', us_uid, us_steamLink, AMOUNT, commission, currency, us_promoCode)
    return JSONResponse(content = {'error': 'Request from not availabled IP or MERCHANT_ID is wrong'}, status_code = status.HTTP_403_FORBIDDEN)

@router.post('/crystalpay', summary = 'Callback for crystalpay payments')
async def index(data: CrystalPayRequest):
    """Callback for crystalpay payments"""

    if data.id and data.currency and data.signature:
        if data.state != 'payed':
            log.debug('privilege not yet been paid')
            return JSONResponse(content = {'error': 'Privilege has not yet been paid'}, status_code = status.HTTP_402_PAYMENT_REQUIRED)

        if data.type != 'purchase':
            log.debug('wrong payment type')
            return JSONResponse(content = {'error': 'Wrong payment type'}, status_code = status.HTTP_402_PAYMENT_REQUIRED)
        
        server_sign = sign_sha1(data.id, os.environ.get('CRYSTALPAY_SECRET2'))

        if server_sign != data.signature:
            log.debug('wrong sign')
            return JSONResponse(content = {'error': 'Wrong sign'}, status_code = status.HTTP_403_FORBIDDEN)

        p_uid = data.extra.split(',')[0]
        p_amount = data.extra.split(',')[1]
        if str(data.amount) != str(p_amount):
            log.debug('wrong amount')
            return JSONResponse(content = {'error': 'Incorrect payment amount'}, status_code = status.HTTP_403_FORBIDDEN)
        p_steam_link = data.extra.split(',')[2]
        p_promo_code = data.extra.split(',')[3]
        return await give_privilege_callback('CrystalPay', p_uid, p_steam_link, data.amount, data.service_commission, data.method, p_promo_code)
    return JSONResponse(content = {'error': 'Request is wrong'}, status_code = status.HTTP_403_FORBIDDEN)

@router.post('/enot', summary = 'Callback for enot payments')
async def index(
    merchant: str = Form(), amount: str = Form(), credited: str = Form(),
    intid: str = Form(), merchant_id: str = Form(), method: str = Form(), sign: str = Form(),
    sign_2: str = Form(), currency: str = Form(), payer_details: str = Form(default=""),
    commission: float = Form(), commission_pay: str = Form(), custom_field: str = Form()):
    """Callback for enot payments

    Args:
        merchant (str): ID вашего магазина  
        amount (float): Сумма заказа
        credited (float): Сумма зачисленная вам на баланс (В рублях)
        intid (int): ID операции в нашей системе
        merchant_id (str): ID операции в вашей системе
        sign (str): Ключ, который вы генерировали до оплаты заказа
        sign_2 (str): Ключ, который сгенерирован, как SIGN, но с секретным ключом №2. Всегда проверяйте данный ключ!
        currency (str): Валюта платежа (RUB, USD, EUR, UAH) (Зависит от валюты магазина. По умолчанию RUB)
        payer_details (str): Реквизиты плательщика (Может быть пустым)
        commission (float): Сумма комиссии при заказе (Зависит от валюты платежа. По умолчанию RUB)
        commission_pay (str): Кто платит комиссию (shop - магазин, client - клиент, 50/50 - 50 на 50)
        custom_field (list|dict|tuple): Строка или массив который вы передавали в параметр "cf"
    """
    if str(merchant) == os.environ.get('ENOT_SHOPID'):
        server_sign_2 = sign_md5(merchant, amount, os.environ.get('ENOT_SECRET2'), merchant_id)
        if server_sign_2 != sign_2:
            log.debug('wrong sign 2 ')
            return JSONResponse(content = {'error': 'Wrong SIGN'}, status_code = status.HTTP_403_FORBIDDEN)
        log.debug('SIGN 2 is valid')
        p_uid = custom_field.split(',')[0]
        p_amount = str(custom_field.split(',')[1])
        new_amount = amount.split('.')[0]
        if str(new_amount) != str(p_amount):
            log.debug('wrong amount')
            return JSONResponse(content = {'error': 'Incorrect payment amount'}, status_code = status.HTTP_403_FORBIDDEN)
        p_steam_link = custom_field.split(',')[2]
        p_promo_code = custom_field.split(',')[3]  
        
        return await give_privilege_callback('Enot.io', p_uid, p_steam_link, new_amount, commission, method, p_promo_code)
    log.debug('request is wrong')
    return JSONResponse(content = {'error': 'Request is wrong'}, status_code = status.HTTP_403_FORBIDDEN)

@router.post('/anypay', summary = 'Callback for anypay payments')
async def index(
    merchant_id: int = Form(), transaction_id: int = Form(default=0), pay_id: int = Form(), amount: int|float = Form(), currency: str = Form(),
    profit: int|float = Form(default=None), email: str = Form(), method: str = Form(default="test"), pay_status: str = Form(alias='status'), test: int = Form(),
    creation_date: str = Form(default='test'), completion_date: str = Form(default='test'),
    sign: str = Form(), field1: str = Form()):
    """Callback for anypay payments

    Args:
        merchant_id (int): ID вашего магазина  
        transaction_id (int): ID платежа
        pay_id (int): ID платежа в системе продавц
        amount (int|float): Сумма заказа
        currency (str): Валюта платежа
        profit (int|float): Сумма зачисленная вам на баланс (В рублях)
        email (str): Email плательщика
        method (str): Способ оплаты
        pay_status (str): Статус платежа в системе AnyPay: paid — оплачен
        test (int): Тестовый платеж или нет (1 — тестовый, 0 — нет)
        creation_date (str): Дата и время создания счета в формате DD.MM.YYYY hh:mm:ss
        completion_date (str): Дата и время обработки счета в формате DD.MM.YYYY hh:mm:ss
        sign (str): Ключ, который вы генерировали до оплаты заказа
        field1 (str): Строка, которую передавали в параметр "custom_field"
    """
    if str(merchant_id) == os.environ.get('ANYPAY_SHOPID'):
        if pay_status != 'paid':
            log.debug('privilege not yet been paid')
            return JSONResponse(content = {'error': 'Privilege has not yet been paid'}, status_code = status.HTTP_402_PAYMENT_REQUIRED)
        server_sign = sign_md5(merchant_id, amount, pay_id, os.environ.get('ANYPAY_SECRET'))
        if server_sign != sign:
            log.debug('wrong sign')
            return JSONResponse(content = {'error': 'Wrong SIGN'}, status_code = status.HTTP_403_FORBIDDEN)
        if profit is not None:
            commission = round(float(amount) - float(profit), 2)
        else:
            commission = 0.0
        p_uid = field1.split(',')[0]
        p_amount = str(field1.split(',')[1])
        if '.' in str(amount):
            amount = str(amount).split('.')[0]
        if str(amount) != str(p_amount):
            log.debug('wrong amount')
            return JSONResponse(content = {'error': 'Incorrect payment amount'}, status_code = status.HTTP_403_FORBIDDEN)
        p_steam_link = field1.split(',')[2]
        p_promo_code = field1.split(',')[3]
        
        return await give_privilege_callback('AnyPay', p_uid, p_steam_link, amount, commission, method, p_promo_code)
    log.debug('request is wrong')
    return JSONResponse(content = {'error': 'Request is wrong'}, status_code = status.HTTP_403_FORBIDDEN)

@router.post('/lava', summary = 'Callback for lava payments')
async def index(request: Request, signature = Header(default="", alias="Authorization")):
    """Callback for lava payments"""
    data = await request.json()
    if signature and data:
        if data['status'] != 'success':
            log.debug('privilege not yet been paid')
            return JSONResponse(content = {'error': 'Privilege has not yet been paid'}, status_code = status.HTTP_402_PAYMENT_REQUIRED)

        secret2 = os.environ.get('LAVA_SECRET2')
        server_sign = sign_hmac_sha256(sort_dict(data), secret2, True)

        if server_sign != signature:
            log.debug(f'WRONG SIGN! Server sign - {server_sign} | request sign - {signature} | Args: {data}')
            return JSONResponse(content = {'error': 'Wrong sign'}, status_code = status.HTTP_403_FORBIDDEN)

        p_uid = data['custom_fields'].split(',')[0]
        p_amount = data['custom_fields'].split(',')[1]
        amount = data['amount']
        if '.' in str(amount):
            amount = str(amount).split('.')[0]
        if str(amount) != str(p_amount):
            log.debug('wrong amount')
            return JSONResponse(content = {'error': 'Incorrect payment amount'}, status_code = status.HTTP_403_FORBIDDEN)

        if data['credited'] != data['amount']:
            commission = round(float(amount) - float(data['credited']), 2)
        else:
            commission = 0.0
        p_steam_link = data['custom_fields'].split(',')[2]
        p_promo_code = data['custom_fields'].split(',')[3]
        return await give_privilege_callback('Lava', p_uid, p_steam_link, amount, commission, data['pay_service'], p_promo_code)
    return JSONResponse(content = {'error': 'Request is wrong'}, status_code = status.HTTP_403_FORBIDDEN)

@router.post('/paypalych', summary = 'Callback for paypalych payments')
async def index(
    InvId: str = Form(), OutSum: float|int = Form(), Commission: float|int = Form(), TrsId: str = Form(), Status: str = Form(),
    CurrencyIn: str = Form(), custom: str = Form(), SignatureValue: str = Form()):
    """Callback for anypay payments

    # ! NOT TESTED

    Args:
        InvId (str): Уникальный идентификатор заказа, переданный при формировании счета
        OutSum (float|int): Сумма платежа
        Commission (float|int): Комиссия с платежа
        TrsId (str): Уникальный идентификатор платежа 
        Status (str): Статус платежа
        CurrencyIn (str): Валюта, в которой оплачивался счет 
        custom (str): Произвольное поле, переданное при формировании счета
        SignatureValue (str): Подпись
    """
    if Status != 'SUCCESS':
        log.debug('privilege not yet been paid')
        return JSONResponse(content = {'error': 'Privilege has not yet been paid'}, status_code = status.HTTP_402_PAYMENT_REQUIRED)
    server_sign = sign_md5_upper(OutSum, InvId, os.environ.get('PAYPALYCH_SECRET'))
    if server_sign != SignatureValue:
        log.debug('wrong sign')
        return JSONResponse(content = {'error': 'Wrong SIGN'}, status_code = status.HTTP_403_FORBIDDEN)
    p_uid = custom.split(',')[0]
    p_amount = str(custom.split(',')[1])
    if '.' in str(OutSum):
        OutSum = str(OutSum).split('.')[0]
    if str(OutSum) != str(p_amount):
        log.debug('wrong amount')
        return JSONResponse(content = {'error': 'Incorrect payment amount'}, status_code = status.HTTP_403_FORBIDDEN)
    p_steam_link = custom.split(',')[2]
    p_promo_code = custom.split(',')[3]
    
    return await give_privilege_callback('Paypalych', p_uid, p_steam_link, OutSum, Commission, 'Paypalych', p_promo_code)
