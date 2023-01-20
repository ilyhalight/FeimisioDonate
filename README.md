# FeimisioDonate System

Не забудьте настроить конфиги и .env файлы в папке с backend и frontend

[![Python Version](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge)](https://www.python.org/) [![NodeJS Version](https://img.shields.io/badge/NodeJS-17-success?style=for-the-badge)](https://nodejs.org/en/) [![GitHub Stars](https://img.shields.io/github/stars/ilyhalight/FeimisioDonate?logo=FemisioStars&style=for-the-badge)](https://github.com/ilyhalight/FeimisioDonate/stargazers) [![GitHub Issues](https://img.shields.io/github/issues/ilyhalight/FeimisioDonate?style=for-the-badge)](https://github.com/ilyhalight/FeimisioDonate/issues) [![Current Version](https://img.shields.io/github/v/release/ilyhalight/FeimisioDonate?style=for-the-badge)](https://github.com/ilyhalight/FeimisioDonate) [![GitHub License](https://img.shields.io/github/license/ilyhalight/FeimisioDonate?style=for-the-badge)](https://github.com/ilyhalight/FeimisioDonate/blob/master/LICENSE)

⭐ Поставьте звездочку на GitHub — это очень мотивирует!

**FeimisioDonate** — Это небольшая система доната для CS:GO серверов. Серверная часть системы построена на Python с использованием FastAPI, а клиенстская часть на NuxtJS 3.0 с использованем TailwindCSS и DaisyUI. Система поддерживает несколько серверов, а также несколько платежных систем.

![FeimisioDonate Preview](https://i.imgur.com/AdWzcnf.png)

---

## 📦 Установка
1. Загрузите репозиторий с GitHub
2. Зайдите в папку *backend* и запустите команду `pip install -r requirements.txt` для установки зависимостей
3. Зайдите в *config/config.cfg* и настройте `chat_id` для телеграм логов
4. Заполните *config/.env* файл по заданному шаблону
5. Запустите сервер командой `python main.py`
6. Зайдите в папку *frontend* и запустите команду `npm install` для установки зависимостей
7. Заполните *.env* файл по заданному шаблону
8. Заполните *config/config.js* по заданному шаблону
9. Соберите клиент командой `npm run build`
10. Запустите клиент командой `npm run start`

---

## 📝 Лицензия
>Вы можете ознакомиться с полной лицензией [здесь](https://github.com/ilyhalight/FeimisioDonate/blob/master/LICENSE)

Этот проект находится под лицензией GPL 3.0. Вы можете использовать его в любых целях, включая коммерческие, но вы должны указывать автора и ссылку на оригинальный репозиторий.