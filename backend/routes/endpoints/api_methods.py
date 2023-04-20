import time
import uuid
import aiohttp
import os
import logging
from fastapi import APIRouter, status, Form
from fastapi.responses import JSONResponse, RedirectResponse
from aiogram.utils.markdown import escape_md

from logger.masslog import MassLog
from config.load import load_cfg
from utils.db import find_privileges_json
from utils.price import get_final_price
from utils.give import give_privilege_callback
from utils.sign import sign_hmac_sha256
from utils.utils import sort_dict

router = APIRouter()
log = logging.getLogger('server')
server_config = load_cfg()['SERVER']

payment_methods_responses = {
    303: {'description': 'Redirected to another page'},
    404: {'description': 'Not found aggregator'},
}

valid_aggregators = [
    'freekassa',
    'enot',
    'crystalpay',
    'anypay',
    'gift',
    'lava',
    'paypalych'
]


@router.post('/payments-methods', response_class = JSONResponse, summary = 'Redirect to another page', responses = payment_methods_responses)
async def index(steam_link: str = Form(), uid: int = Form(), selectedMethod: str = Form(), promocode: str = Form(default = '')):
    log.debug('Redirect to another page')
    if ';' in selectedMethod:
        aggregator = selectedMethod.split(';')[0]
        selectedMethod = selectedMethod.split(';')[1]
    else:
        aggregator = selectedMethod
        selectedMethod = ''
    if aggregator in valid_aggregators and uid > 0:
        privilege = await find_privileges_json(uid)
        privilege_name = ''
        if privilege:
            price_clear = privilege['price']
            discount = privilege['discount']
            privilege_name = privilege['name']
            log.debug(promocode)
            price = await get_final_price(price_clear, discount, promocode)
        else:
            return JSONResponse(content = {'error': 'Not valid uid'}, status_code = status.HTTP_404_NOT_FOUND)
        if price > 0:
            await MassLog().info(f'[Пользователь]({steam_link}) создал ссылку на оплату **{escape_md(privilege_name)}** \(UID: **{uid}**\) за **{escape_md(price)}** руб\. \(скидка: **{escape_md(discount)}**% \| платежка: **{escape_md(aggregator)}** \| промокод: **{escape_md(promocode)}**\)')
            if 'id' in steam_link:
                steam_arr = steam_link.split('/id/')
                steam_arr = f'id{steam_arr[-1]}'.replace('/', '')
            elif 'profiles' in steam_link:
                steam_arr = steam_link.split('/profiles/')
                steam_arr = f'profiles{steam_arr[-1]}'.replace('/', '')
            else:
                steam_arr = f'{steam_link}'

            match aggregator:
                case 'crystalpay':
                    shopid = os.environ.get('CRYSTALPAY_SHOPID')
                    secret = os.environ.get('CRYSTALPAY_SECRET')
                    async with aiohttp.ClientSession() as session:
                        async with session.post('https://api.crystalpay.io/v2/invoice/create/', json = {
                            'auth_login': shopid,
                            'auth_secret': secret,
                            'amount': price,
                            'type': 'purchase',
                            'description': server_config['donate_description'],
                            'redirect_url': f'{server_config["site_donate_domain"]}/results/success',
                            'callback_url': f'{server_config["site_api_domain"]}/api/callback/crystalpay',
                            'lifetime': 30,
                            'extra': f'{uid},{price},{steam_arr},{promocode}'
                        }) as resp:
                            data = await resp.json(content_type=None)
                            if data and data['error'] == False and data['url'] != '':
                                return RedirectResponse(url = data['url'], status_code = status.HTTP_303_SEE_OTHER)
                            await MassLog().error(f'Ошибка при создании ссылки на оплату через **CrystalPay**: {escape_md(str(data))}')
                            return JSONResponse(content = {'error': 'Server error'}, status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
                case 'lava':
                    shopid = os.environ.get('LAVA_SHOPID')
                    secret = os.environ.get('LAVA_SECRET')

                    data_json = {
                        'sum': price,
                        'orderId': uuid.uuid4().hex,
                        'shopId': shopid,
                        'expire': 300,
                        'failUrl': f'{server_config["site_donate_domain"]}/results/error',
                        'successUrl': f'{server_config["site_donate_domain"]}/results/success',
                        'hookUrl': f'{server_config["site_api_domain"]}/api/callback/lava',
                        'includeService': [
                            'card',
                            'sbp',
                            'qiwi'
                        ],
                        'customFields': f'{uid},{price},{steam_arr},{promocode}',
                        'comment': server_config['donate_description']
                    }

                    data_json = sort_dict(data_json)
                    sign = sign_hmac_sha256(data_json, secret)
                    
                    async with aiohttp.ClientSession() as session:
                        async with session.post('https://api.lava.ru/business/invoice/create',
                            json = data_json,
                            headers = {
                                'Signature': sign,
                                'Accept': 'application/json',
                                'Content-Type': 'application/json'
                            }
                        ) as resp:
                            data = await resp.json(content_type=None)
                            if data and data['status_check'] == True and data['data'] is not None:
                                return RedirectResponse(url = data['data']['url'], status_code = status.HTTP_303_SEE_OTHER)
                            await MassLog().error(f'Ошибка при создании ссылки на оплату через **Lava**: {escape_md(str(data))}')
                            return JSONResponse(content = {'error': 'Server error'}, status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
                case 'paypalych':
                    secret = os.environ.get('PAYPALYCH_SECRET')
                    shopid = os.environ.get('PAYPALYCH_SHOPID')
                    currency = 'RUB'
                    if aggregator == 'another_cards':
                        currency = 'USD'
                    async with aiohttp.ClientSession() as session:
                        async with session.post('https://paypalych.com/api/v1/bill/create',
                            params = {
                                'amount': price,
                                'order_id': uuid.uuid4().hex,
                                'description': server_config['donate_description'],
                                'type': 'normal',
                                'shop_id': shopid,
                                'currency_in': currency,
                                'custom': f'{uid},{price},{steam_arr},{promocode}',
                                'payer_pays_commission': 1,
                                'name': 'Донат',
                                'success_url':  f'{server_config["site_donate_domain"]}/results/success',
                                'fail_url': f'{server_config["site_donate_domain"]}/results/error',
                            },
                            headers = {
                                'Authorization': f'Bearer {secret}',
                            }
                        ) as resp:
                            data = await resp.json(content_type=None)
                            print(data)
                            if data and data['success'] == "true":
                                return RedirectResponse(url = data['link_page_url'], status_code = status.HTTP_303_SEE_OTHER)
                            await MassLog().error(f'Ошибка при создании ссылки на оплату через **PayPalych**: {escape_md(str(data))}')
                            return JSONResponse(content = {'error': 'Server error'}, status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
                case _:
                    currency = 'RUB'
                    if aggregator == 'another_cards':
                        currency = 'USD'
                    return RedirectResponse(url = f'{server_config["site_donate_domain"]}/payments/{aggregator}?steam={steam_arr}&price={price}&uid={uid}&currency={currency}&promocode={promocode}', status_code = status.HTTP_303_SEE_OTHER)
        elif price == 0:
            return await give_privilege_callback('Без оплаты', uid, steam_link, 0, 0, 'Бесплатно', promocode)
        else:
            return JSONResponse(content = {'error': 'Not valid price'}, status_code = status.HTTP_404_NOT_FOUND)
    else:
        return JSONResponse(content = {'error': 'Not valid aggregator'}, status_code = status.HTTP_404_NOT_FOUND)