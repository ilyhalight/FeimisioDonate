# FeimisioDonate System

[![Python Version](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge)](https://www.python.org/) [![NodeJS Version](https://img.shields.io/badge/NodeJS-18-success?style=for-the-badge)](https://nodejs.org/en/) [![GitHub Stars](https://img.shields.io/github/stars/ilyhalight/FeimisioDonate?logo=FemisioStars&style=for-the-badge)](https://github.com/ilyhalight/FeimisioDonate/stargazers) [![GitHub Issues](https://img.shields.io/github/issues/ilyhalight/FeimisioDonate?style=for-the-badge)](https://github.com/ilyhalight/FeimisioDonate/issues) [![Current Version](https://img.shields.io/github/v/release/ilyhalight/FeimisioDonate?style=for-the-badge)](https://github.com/ilyhalight/FeimisioDonate) [![GitHub License](https://img.shields.io/github/license/ilyhalight/FeimisioDonate?style=for-the-badge)](https://github.com/ilyhalight/FeimisioDonate/blob/master/LICENSE)

⭐ Поставьте звездочку на GitHub — это очень мотивирует!

**FeimisioDonate** — Это небольшая система доната для CS:GO серверов. Серверная часть системы построена на Python с использованием FastAPI, а клиентская часть на NuxtJS 3.0. Система поддерживает несколько серверов, а также несколько платежных систем.

![FeimisioDonate Preview](https://i.imgur.com/A2Q5nIC.png)


## 📖 Доступные платежные системы
Все платежные системы включаются вручную, через базу данных. Список доступных платежных систем:
| Платежная система | Статус | Имя в БД |
|---|---|---
| [Freekassa](https://freekassa.ru/) | ✅ | freekassa |
| [Enot.io](https://enot.io/) | ✅ | enot |
| [AnyPay](https://anypay.io/) | ✅ | anypay |
| [Lava](https://lava.ru) | ✅ | lava |
| [CrystalPay](https://crystalpay.io/) | ✅ | crystalpay |
| [PayPalych](https://paypalych.com/) | NOT TESTED | paypalych |

Примечание: Алгоритм подписи платежной системы AnyPay должен быть установлен на MD5.

---

## 📦 Установка
1. Загрузите репозиторий с GitHub
2. Зайдите в папку *backend* и запустите команду `pip install -r requirements.txt` для установки зависимостей
3. Зайдите в *config/config.cfg* и настройте `chat_id` для телеграм логов, а так же ссылки расположение сайта
4. Заполните *config/.env* файл по заданному шаблону
5. Запустите сервер командой `python main.py`
6. Зайдите в папку *frontend* и запустите команду `npm install` для установки зависимостей
7. Заполните *.env* файл по заданному шаблону (если нужен кастомный порт)
8. Заполните *config/config.js* по заданному шаблону
9. Установите свои ключевые слова (keywords) и пути к сертификатам (если собираетесь размещать сайт на домене) в файле *nuxt.config.js*
10. Соберите клиент командой `npm run build`
11. Установите *pm2* командой `npm install pm2 -g && pm2 install pm2-logrotate`
12. Запустите клиент командой `pm2 start ecosystem.config.js`

---

## 📝 Лицензия
>Вы можете ознакомиться с полной лицензией [здесь](https://github.com/ilyhalight/FeimisioDonate/blob/master/LICENSE)

Этот проект находится под лицензией GPL 3.0. Вы можете использовать его в любых целях, включая коммерческие, но вы должны указывать автора и ссылку на оригинальный репозиторий.