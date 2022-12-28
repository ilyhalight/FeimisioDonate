## Поддержимаемые плагины для CS:GO
Для использования того или иного плагина необходимо отредактировать код. По умолчанию выдача включена сразу для двух плагинов.
- VIP Core 3.0 от R1KO
- MaterialAdmin (возможно и SourceBans++) 



## 1. Заполнить **Конфиг** сайта
- Путь: `config/config.cfg`
- Описание: Конфигурационный файл сайта, содержащий дополнительные настройки

```
[LEVEL]
telegram - Логировать ли в Telegram
discord - Логировать ли в Discord
rich - Форматировать ли логи с помощью библиотеки rich
server_lvl - Уровень логирования # Возможные значения: 10, 20, 30, 40, 50 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
server_save - Сохранять ли логи
telegram_lvl - Уровень логирования # Возможные значения: 10, 20, 30, 40, 50 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
telegram_save - Уровень логирования # Возможные значения: 10, 20, 30, 40, 50 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
discord_lvl - Уровень логирования # Возможные значения: 10, 20, 30, 40, 50 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
discord_save - Уровень логирования # Возможные значения: 10, 20, 30, 40, 50 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
```

```
[DISCORD]
username - Имя вебхука (может быть пустой строкой)
avatar_url - Ссылка на аватарку вебхука (может быть пустой строкой)
allowed_mentions - Разрешить ли упоминания через вебхук
```

```
[TELEGRAM]
chat_id - ID чата, в которое бот пришлет сообщение
parse_mode - Тип форматирования сообщения. По умолчанию MarkDownV2 # Возможные значения: MarkdownV2, HTML, Markdown (https://core.telegram.org/bots/api#formatting-options)
disable_web_page_preview - Отключить предпросмотр ссылок
disable_notification - Отключить уведомления от сообщений
```

## 2. Заполнить **.env** файл
SECRET - Секретный ключ для шифрования данных
