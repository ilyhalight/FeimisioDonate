import aiohttp
import os
import logging
from fastapi import APIRouter, status, Form
from fastapi.responses import JSONResponse, RedirectResponse
from aiogram.utils.markdown import escape_md

from sql.promocode_uses.controller import DbPromocodeUsesController
from logger.masslog import MassLog
from utils.db import find_privilleges_json, find_promocodes_json

router = APIRouter()
log = logging.getLogger('server')

payment_methods_responses = {
    303: {'description': 'Redirected to another page'},
    404: {'description': 'Not found aggregator'},
}


@router.post('/payments-methods', response_class = JSONResponse, summary = 'Redirect to another page', responses = payment_methods_responses)
async def index(steam_link: str = Form(), uid: int = Form(), aggregator: str = Form(), promocode: str = Form(default = '')):
    log.debug('Redirect to another page')
    if aggregator in ['freekassa', 'enot', 'crystalpay'] and uid > 0:
        privillege = await find_privilleges_json(uid)
        privillege_name = ''
        if privillege:
            price_clear = privillege['price']
            discount = privillege['discount']
            privillege_name = privillege['name']
            log.debug(promocode)
            if promocode != '' and discount > 0 and price_clear > 0:
                price = round(price_clear - (price_clear / 100 * discount))
                promo_info = await find_promocodes_json(promocode)
                if promo_info and promo_info['discount']:
                    promo_uses = await DbPromocodeUsesController().get_by_key(promocode)
                    if price_clear <= promo_info['min_price'] or price_clear > promo_info['max_price']:
                        pass
                    elif len(promo_uses) > promo_info['uses']:
                        pass
                    else:
                        price = round(price - (price / 100 * promo_info['discount']))
            elif discount > 0 and price_clear > 0 and promocode == '':
                price = round(price_clear - (price_clear / 100 * discount))
            elif promocode != '' and price_clear > 0:
                promo_info = await find_promocodes_json(promocode)
                if promo_info and promo_info['discount']:
                    promo_uses = await DbPromocodeUsesController().get_by_key(promocode)
                    if price_clear <= promo_info['min_price'] or price_clear > promo_info['max_price']:
                        price = price_clear
                    elif len(promo_uses) > promo_info['uses']:
                        price = price_clear
                    else:
                        price = round(price_clear - (price_clear / 100 * promo_info['discount']))
                else:
                    price = price_clear
            else:
                price = price_clear
        else:
            return JSONResponse(content = {'error': 'Not valid uid'}, status_code = status.HTTP_404_NOT_FOUND)
        if price > 0:
            await MassLog().info(f'[Пользователь]({steam_link}) создал ссылку на оплату **{escape_md(privillege_name)}** \(UID: **{uid}**\) за **{escape_md(price)}** руб\. \(скидка: **{escape_md(discount)}**% \| платежка: {escape_md(aggregator)}\ \| промокод: {escape_md(promocode)}\)')
            if 'id' in steam_link:
                steam_arr = steam_link.split('/id/')
                steam_arr = f'id{steam_arr[-1]}'
            elif 'profiles' in steam_link:
                steam_arr = steam_link.split('/profiles/')
                steam_arr = f'profiles{steam_arr[-1]}'
            else:
                steam_arr = f'{steam_link}'
            if aggregator != 'crystalpay':
                return RedirectResponse(url = f'http://localhost:3999/payments/{aggregator}?steam={steam_arr}&price={price}&uid={uid}&promocode={promocode}', status_code = status.HTTP_303_SEE_OTHER)
            else:
                crystalpay_shopid = os.environ.get('CRYSTALPAY_SHOPID')
                crystalpay_secret = os.environ.get('CRYSTALPAY_SECRET')
                async with aiohttp.ClientSession() as session:
                    async with session.get('https://api.crystalpay.ru/v1/', params = {
                        'o': 'invoice-create',
                        'n': crystalpay_shopid,
                        's': crystalpay_secret,
                        'amount': price,
                        'lifetime': 30,
                        'extra': f'{uid},{price},{steam_arr}'
                    }) as resp:
                        data = await resp.json()
                        if data and data['auth'] == 'ok' and data['error'] == False and data['url'] != '':
                            return RedirectResponse(url = data['url'], status_code = status.HTTP_303_SEE_OTHER)
                        await MassLog().error(f'Ошибка при создании ссылки на оплату через **CrystalPay**: {escape_md(str(data))}')
                        return JSONResponse(content = {'error': 'Server error'}, status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            await MassLog().info(f'[Пользователь]({steam_link}) получил бесплатную привилегию {escape_md(privillege_name)} \(промокод: {escape_md(promocode)}\)')
            return JSONResponse(content = {'error': 'WIP'}, status_code = status.HTTP_306_RESERVED)
    else:
        return JSONResponse(content = {'error': 'Not valid aggregator'}, status_code = status.HTTP_404_NOT_FOUND)