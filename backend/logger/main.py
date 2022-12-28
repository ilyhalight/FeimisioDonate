from datetime import datetime
import logging
import os
import sys
import rich

from rich.logging import RichHandler
from rich.theme import Theme
from rich.style import Style

from config.load import load_cfg


settings = load_cfg()['LOGGING']

def init_logging():
    root_logger = logging.getLogger()
    base_logger = logging.getLogger("server")
    discord_logger = logging.getLogger('discord')
    telegram_logger = logging.getLogger('telegram')
    worker_logger = logging.getLogger('worker')

    logs = [base_logger, worker_logger, discord_logger, telegram_logger]
    for log in logs:
        if log.name.replace('.', '_') + '_lvl' in settings and settings[log.name.replace('.', '_') + '_lvl'] in [10, 20, 30, 40, 50]:
            log.setLevel(settings[log.name.replace('.', '_') + '_lvl'])

    file_formatter = logging.Formatter(
        '[{asctime}] [{levelname}] {module}-{name}: {message}', datefmt = '%Y-%m-%d %H:%M:%S', style = '{'
    )

    if settings['rich']:
        rich_console = rich.get_console()
        rich.reconfigure(tab_size = 4)
        # Theme from https://github.com/Cog-Creators/Red-DiscordBot/blob/V3/develop/redbot/logging.py
        rich_console.push_theme(Theme(
            {
                    'log.time': Style(dim = True),
                    'logging.level.warning': Style(color = 'yellow'),
                    'logging.level.critical': Style(color = 'white', bgcolor = 'red'),
                    'logging.level.error': Style(color = 'red'),
                    'logging.level.verbose': Style(color = 'magenta', italic = True, dim = True),
                    'logging.level.trace': Style(color = 'white', italic = True, dim = True),
                    'repr.number': Style(color = 'cyan'),
                    'repr.url': Style(underline = True, italic = True, bold = False, color = 'cyan'),
            }
        ))
        rich_console.file = sys.stdout
        rich_formatter = logging.Formatter('{message}', datefmt = '[%X]', style = '{')
        stdout_handler = RichHandler(
            rich_tracebacks = True
        )
        stdout_handler.setFormatter(rich_formatter)
    else:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(file_formatter)

    root_logger.addHandler(stdout_handler)
    logging.captureWarnings(True)

    if not os.path.isdir('./logs'):
        try:
            os.mkdir('./logs')
            root_logger.info('Creating log directory')
        except OSError as err:
            root_logger.error(f'Failed to create log directory: {err}')

    part = f'_{datetime.now().strftime("%Y%m%d")}'

    for log in logs:
        if log.name.replace('.', '_') + '_save' in settings and settings[log.name.replace('.', '_') + '_save']:
            if os.path.isfile(f'./logs/{log.name.replace(".", "_")}{part}.log'):
                file_mode = 'a'
            else:
                file_mode = 'w'
            logger_handler = logging.FileHandler(f'./logs/{log.name.replace(".", "_")}{part}.log', encoding='utf8', mode = file_mode)
            logger_handler.setFormatter(file_formatter)
            log.addHandler(logger_handler)

    return True
