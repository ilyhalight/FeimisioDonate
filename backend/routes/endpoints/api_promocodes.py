import logging
import os
from fastapi import APIRouter, status, Header
from fastapi.responses import JSONResponse

from models.promocode_uses import PromocodeUses
from models.promocodes import Promocodes
from sql.promocode_uses.controller import DbPromocodeUsesController
from utils.db import get_promocodes_json
from utils.token import validate_token

router = APIRouter()
log = logging.getLogger('server')

get_promocodes_responses = {
    200: {'description': 'OK', 'model': list[Promocodes]},
    204: {'description': 'No content'},
    404: {'description': 'Not Found'},
}

get_promocodes_uses_responses = {
    200: {'description': 'OK', 'model': list[PromocodeUses]},
    204: {'description': 'No content'},
    404: {'description': 'Not Found'},
}

@router.get('/promocodes', response_class = JSONResponse, summary = 'Get promocodes', responses = get_promocodes_responses)
async def index(authorization: str = Header(default = '')):
    log.debug('Getting promocodes')
    if authorization != '' and len(authorization.split(',')) > 1:
        keys = authorization.split(',')
        key = os.environ.get('FEIMISIO_PROMOCODES_KEY')
        timestamp = int(keys[0])
        token = keys[1]
        is_valid = await validate_token(token, key, timestamp)
        if is_valid:
            promocodes = await get_promocodes_json()
            if promocodes:
                return JSONResponse(content = promocodes, status_code = status.HTTP_200_OK)
            return JSONResponse(content = {'error': 'No data found'}, status_code = status.HTTP_204_NO_CONTENT)
    return JSONResponse(content = {'error': 'Invalid token'}, status_code = status.HTTP_401_UNAUTHORIZED)

@router.get('/promocodes/uses', response_class = JSONResponse, summary = 'Get promocode uses', responses = get_promocodes_uses_responses)
async def index(promo: str = '', authorization: str = Header(default = '')):
    log.debug('find promocodes uses')
    if authorization != '' and len(authorization.split(',')) > 1:
        keys = authorization.split(',')
        key = os.environ.get('FEIMISIO_PROMOCODES_KEY')
        timestamp = int(keys[0])
        token = keys[1]
        is_valid = await validate_token(token, key, timestamp)
        if is_valid:
            if promo == '':
                data = await DbPromocodeUsesController().get_all()
            else:
                data = await DbPromocodeUsesController().get_by_key(promo)
            if data and len(data) > 0:
                return JSONResponse(content = data, status_code = status.HTTP_200_OK)
            return JSONResponse(content = {'error': 'No data found'}, status_code = status.HTTP_204_NO_CONTENT)
    return JSONResponse(content = {'error': 'Invalid token'}, status_code = status.HTTP_401_UNAUTHORIZED)