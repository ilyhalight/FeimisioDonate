import logging
from config.load import load_cfg

from logger.telegram import TelegramLogger
from logger.discord import DiscordLogger

class MassLog:
    def __init__(self, logging_lib: bool = True):
        self.log_cfg = load_cfg()['LOGGING']
        self.logging_lib = logging_lib # Использовать ли логирование с помощью logging

    async def log_by_type(self, type: str, text: str):
        if type == 'success':
            await MassLog().success(text)
        elif type == 'error':
            await MassLog().error(text)
        elif type == 'warning' or type == 'warn':
            await MassLog().warn(text)
        else:
            await MassLog().info(text)

    async def info(self, text: str):
        if self.logging_lib:
            log = logging.getLogger('server')
            log.info(text)
        tg_status = None
        ds_status = None
        if self.log_cfg['telegram']:
            tg_status = await TelegramLogger().info(text)
        if self.log_cfg['discord']:
            ds_status = await DiscordLogger().info(text)
        return {
            'method': 'info',
            'telegram': tg_status if type(tg_status) is bool else tg_status['ok'],
            'discord': ds_status
        }

    async def warn(self, text: str):
        if self.logging_lib:
            log = logging.getLogger('server')
            log.warn(text)
        tg_status = None
        ds_status = None
        if self.log_cfg['telegram']:
            tg_status = await TelegramLogger().warn(text)
        if self.log_cfg['discord']:
            ds_status = await DiscordLogger().warn(text)
        return {
            'method': 'warn',
            'telegram': tg_status if type(tg_status) is bool else tg_status['ok'],
            'discord': ds_status
        }

    async def error(self, text: str):
        if self.logging_lib:
            log = logging.getLogger('server')
            log.error(text)
        tg_status = None
        ds_status = None
        if self.log_cfg['telegram']:
            tg_status = await TelegramLogger().error(text)
        if self.log_cfg['discord']:
            ds_status = await DiscordLogger().error(text)
        return {
            'method': 'error',
            'telegram': tg_status if type(tg_status) is bool else tg_status['ok'],
            'discord': ds_status
        }

    async def success(self, text: str):
        if self.logging_lib:
            log = logging.getLogger('server')
            log.info(text)
        tg_status = None
        ds_status = None
        if self.log_cfg['telegram']:
            tg_status = await TelegramLogger().success(text)
        if self.log_cfg['discord']:
            ds_status = await DiscordLogger().success(text)
        return {
            'method': 'success',
            'telegram': tg_status if type(tg_status) is bool else tg_status['ok'],
            'discord': ds_status
        }