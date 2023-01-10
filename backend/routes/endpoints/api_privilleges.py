import logging
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from models.privillege import Privillege
from models.privillege_info import PrivillegeInfo
from utils.db import get_privilleges_json, find_privilleges_json, find_privilleges_info_json

router = APIRouter()
log = logging.getLogger('server')

get_privilleges_responses = {
    200: {'description': 'OK', 'model': list[Privillege]},
    204: {'description': 'No content'},
    404: {'description': 'Not Found'},
}

get_privillege_info_responses = {
    200: {'description': 'OK', 'model': list[PrivillegeInfo]},
    204: {'description': 'No content'},
    404: {'description': 'Not Found'},
}

@router.get('/privilleges', response_class = JSONResponse, summary = 'Get privilleges', responses = get_privilleges_responses)
async def index():
    log.debug('Getting privilleges')
    privilleges = await get_privilleges_json()
    if privilleges:
        return JSONResponse(content = privilleges, status_code = status.HTTP_200_OK)
    return JSONResponse(content = {'error': 'No data found'}, status_code = status.HTTP_204_NO_CONTENT)

@router.get('/privillege', response_class = JSONResponse, summary = 'Get privilleges', responses = get_privilleges_responses)
async def index(uid: int):
    log.debug('find privilleges')
    privilleges = await find_privilleges_json(uid)
    if privilleges:
        return JSONResponse(content = privilleges, status_code = status.HTTP_200_OK)
    return JSONResponse(content = {'error': 'No data found'}, status_code = status.HTTP_204_NO_CONTENT)

@router.get('/privillege/info', response_class = JSONResponse, summary = 'Get privillege info', responses = get_privillege_info_responses)
async def index(name: str):
    log.debug('find privillege info')
    data = await find_privilleges_info_json(name)
    if data:
        return JSONResponse(content = data, status_code = status.HTTP_200_OK)
    return JSONResponse(content = {'error': 'No data found'}, status_code = status.HTTP_204_NO_CONTENT)