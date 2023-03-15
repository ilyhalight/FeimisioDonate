import logging
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from models.privilege import Privilege
from models.privilege_info import PrivilegeInfo
from utils.db import get_privileges_json, find_privileges_json, find_privileges_info_json

router = APIRouter()
log = logging.getLogger('server')

get_privileges_responses = {
    200: {'description': 'OK', 'model': list[Privilege]},
    204: {'description': 'No content'},
    404: {'description': 'Not Found'},
}

get_privilege_info_responses = {
    200: {'description': 'OK', 'model': list[PrivilegeInfo]},
    204: {'description': 'No content'},
    404: {'description': 'Not Found'},
}

@router.get('/privileges', response_class = JSONResponse, summary = 'Get privileges', responses = get_privileges_responses)
async def index():
    log.debug('Getting privileges')
    privileges = await get_privileges_json()
    if privileges:
        return JSONResponse(content = privileges, status_code = status.HTTP_200_OK)
    return JSONResponse(content = {'error': 'No data found'}, status_code = status.HTTP_204_NO_CONTENT)

@router.get('/privilege', response_class = JSONResponse, summary = 'Get privileges', responses = get_privileges_responses)
async def index(uid: int):
    log.debug('find privileges')
    privileges = await find_privileges_json(uid)
    if privileges:
        return JSONResponse(content = privileges, status_code = status.HTTP_200_OK)
    return JSONResponse(content = {'error': 'No data found'}, status_code = status.HTTP_204_NO_CONTENT)

@router.get('/privilege/info', response_class = JSONResponse, summary = 'Get privilege info', responses = get_privilege_info_responses)
async def index(name: str):
    log.debug('find privilege info')
    data = await find_privileges_info_json(name)
    if data:
        return JSONResponse(content = data, status_code = status.HTTP_200_OK)
    return JSONResponse(content = {'error': 'No data found'}, status_code = status.HTTP_204_NO_CONTENT)