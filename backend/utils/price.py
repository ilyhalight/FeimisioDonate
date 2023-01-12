from sql.promocode_uses.controller import DbPromocodeUsesController
from utils.db import find_promocodes_json


async def get_final_price(price_clear, discount, promocode):
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
    return price