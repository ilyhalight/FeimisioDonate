import logging
import os
import aiohttp
from datetime import datetime

from config.load import load_cfg


class DiscordLogger:
    def __init__(self):
        self.discord_cfg = load_cfg()['DISCORD']
        self.log = logging.getLogger('discord')
        self.webhook = os.environ.get('DISCORD_WEBHOOK')
        self.username = self.discord_cfg['username']
        self.avatar_url = self.discord_cfg['avatar_url'] if self.discord_cfg['avatar_url'] else None
        self.allowed_mentions = self.discord_cfg['allowed_mentions']

    async def log_default(self, color: str, message: list|str):
        """Отправляет сообщение в Discord
        
        Args:
            color(str): Цвет сообщения (decimal color) # hex to decimal https://www.mathsisfun.com/hexadecimal-decimal-colors.html
            message(list|str): Сообщение
        """
        if type(message) is not list:
            if type(message) is str:
                message = {
                    'title': 'Уведомление',
                    'description': message,
                }
            elif type(message) is dict:
                pass
            else:
                raise TypeError('Message must be a json, list, dict or a string')
        if not self.webhook:
            raise TypeError('Discord Webhook not found')
        async with aiohttp.ClientSession() as session:
            json_params = {
                'username': self.username,
                'embeds': [{
                    'title': message['title'],
                    'description': message['description'],
                    'timestamp': datetime.utcnow().isoformat(),
                    'color': color
                }],
                'avatar_url': self.avatar_url,
                'allowed_mentions': self.allowed_mentions
            }
            async with session.post(self.webhook, json = json_params) as resp:
                return True if resp.status in [200, 204] else False
    
    async def info(self, message: str):
        """Отправляет информационное сообщение в Discord"""
        try:
            res = await self.log_default('5986543', message)
            return res
        except TypeError as err:
            self.log.error(err)
            return False
        except Exception as err:
            self.log.exception(err)
            return False

    async def warn(self, message: str):
        """Отправляет предупреждение в Discord"""
        try:
            message = {
                'title': f'⚠ Предупреждение',
                'description': message,
            }
            res = await self.log_default('16762193', message)
            return res
        except TypeError as err:
            self.log.error(err)
            return False
        except Exception as err:
            self.log.exception(err)
            return False

    async def error(self, message: str):
        """Отправляет ошибку в Discord"""
        try:
            message = {
                'title': f'❗ Ошибка',
                'description': message,
            }
            res = await self.log_default('16733491', message)
            return res
        except TypeError as err:
            self.log.error(err)
            return False
        except Exception as err:
            self.log.exception(err)
            return False

    async def success(self, message: str):
        """Отправляет успешное сообщение в Discord"""
        try:
            message = {
                'title': f'✅ Успех',
                'description': message,
            }
            res = await self.log_default('4177727', message)
            return res
        except TypeError as err:
            self.log.error(err)
            return False
        except Exception as err:
            self.log.exception(err)
            return False