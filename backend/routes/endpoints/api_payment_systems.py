import logging
import os
from fastapi import APIRouter, status, Header
from fastapi.responses import JSONResponse

from models.payment_system import PaymentSystem
from utils.db import get_payment_systems_json
from utils.token import validate_token

router = APIRouter()
log = logging.getLogger('server')

get_payment_systems_responses = {
    200: {'description': 'OK', 'model': list[PaymentSystem]},
    204: {'description': 'No content'},
    404: {'description': 'Not Found'},
}

@router.get('/payment-systems', response_class = JSONResponse, summary = 'Get payment systems', responses = get_payment_systems_responses)
async def index(authorization: str = Header(default = '')):
    log.debug('Getting payment systems')
    if authorization != '' and len(authorization.split(',')) > 1:
        keys = authorization.split(',')
        key = os.environ.get('FEIMISIO_PROMOCODES_KEY')
        timestamp = int(keys[0])
        token = keys[1]
        is_valid = await validate_token(token, key, timestamp)
        if is_valid:
            payment_systems = await get_payment_systems_json()
            if payment_systems:
                return JSONResponse(content = payment_systems, status_code = status.HTTP_200_OK)
            return JSONResponse(content = {'error': 'No data found'}, status_code = status.HTTP_204_NO_CONTENT)
    return JSONResponse(content = {'error': 'Invalid token'}, status_code = status.HTTP_401_UNAUTHORIZED)