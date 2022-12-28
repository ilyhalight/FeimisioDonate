import logging
import os
import aiohttp

from config.load import load_cfg


class TelegramLogger:
    def __init__(self):
        self.telegram_cfg = load_cfg()['TELEGRAM']
        self.log = logging.getLogger('telegram')
        self.chat_id = self.telegram_cfg['chat_id']
        self.parse_mode = self.telegram_cfg['parse_mode'] or 'MarkdownV2'
        self.disable_web_page_preview = self.telegram_cfg['disable_web_page_preview']
        self.disable_notification = self.telegram_cfg['disable_notification']
        self.token = os.environ.get('TELEGRAM_TOKEN')

    # def escape_specialchars(self, message: str):
    #     """Экранирует спецсимволы в сообщении"""
    #     message = message.replace('(', '\\(')
    #     message = message.replace(')', '\\)')
    #     message = message.replace('.', '\\.')
    #     message = message.replace('|', '\\|')
    #     return message

    async def log_default(self, message: str):
        """Отправляет сообщение в Telegram
        
        Args:
            color(str): Цвет сообщения (decimal color)
            message(list|str): Сообщение
        """
        if not self.token:
            raise TypeError('Telegram Token not found')
        async with aiohttp.ClientSession() as session:
            json_params = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': self.parse_mode,
                'disable_web_page_preview': self.disable_web_page_preview,
                'disable_notification': self.disable_notification,
            }
            async with session.post(f'https://api.telegram.org/bot{self.token}/sendMessage', json = json_params) as resp:
                return await resp.json()
    
    async def info(self, message: str):
        """Отправляет информационное сообщение в Telegram"""
        try:
            res = await self.log_default(message)
            if res['ok'] == False:
                self.log.error(res)
            return res
        except TypeError as err:
            self.log.error(err)
            return False
        except Exception as err:
            self.log.exception(err)
            return False

    async def warn(self, message: str):
        """Отправляет предупреждение в Telegram"""
        try:
            if type(message) is str:
                message = f'⚠️ Предупреждение\n{message}'
            res = await self.log_default(message)
            if res['ok'] == False:
                self.log.error(res)
            return res
        except TypeError as err:
            self.log.error(err)
            return False
        except Exception as err:
            self.log.exception(err)
            return False

    async def error(self, message: str):
        """Отправляет ошибку в Telegram"""
        try:
            if type(message) is str:
                message = f'❗Ошибка\n{message}'
            res = await self.log_default(message)
            if res['ok'] == False:
                self.log.error(res)
            return res
        except TypeError as err:
            self.log.error(err)
            return False
        except Exception as err:
            self.log.exception(err)
            return False

    async def success(self, message: str):
        """Отправляет успешное сообщение в Telegram"""
        try:
            if type(message) is str:
                message = f'✅ Успех\n{message}'
            res = await self.log_default(message)
            if res['ok'] == False:
                self.log.error(res)
            return res
        except TypeError as err:
            self.log.error(err)
            return False
        except Exception as err:
            self.log.exception(err)
            return False