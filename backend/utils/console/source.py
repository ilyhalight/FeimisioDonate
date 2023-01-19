import logging
from rcon.source import rcon

log = logging.getLogger('server')

# For CS:GO, mb CS:S
async def add_vip_ingame(ip: str, port: int, rcon_password: str, steamid: str, group: str, seconds: str|int):
    """add vip to ingame server (vip_core 3.0)
    
    Args:
        ip (str): server ip
        port (int): server port
        rcon_password (str): rcon password
        steamid (str): steamid (steamID формата STEAM_1:0:424055351)
        group (str): vip group (из groups.ini)
        seconds (str): seconds
    """
    response = await rcon(f'sm_addvip "#{steamid}" "{group}" "{seconds}"', host = ip, port = port, passwd = rcon_password)
    if response == '[SM] Не найден подходящий игрок' or '[VIP] Неверное использование!' in response:
        response = False
    log.info(f'Результат добавления VIP: {response}')
    return response


if __name__ == '__main__':
    import asyncio
    asyncio.run(add_vip_ingame('185.248.100.95', 27101, 'rcon_pass', 'STEAM_1:0:424055351', 'Premium', 0))

# [SM] Не найден подходящий игрок
# sm_addvip "#STEAM_1:1:636193233" "VIP" "60"
# VIP-Игрок onebg (STEAM_1:1:636193233, 151.249.175.30) (ID: 1272386467) успешно добавлен!
# L 12/19/2022 - 19:16:31: [vip/VIP_Core.smx] VIP-Игрок onebg (STEAM_1:1:636193233, 151.249.175.30) (ID: 1272386467, Длительность: 01:00, Истек