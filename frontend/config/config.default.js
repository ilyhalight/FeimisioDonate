const config = () => {
    return {
        'feimisioToken': '', // Токен для авторизации на сервере (должен быть такой же как в backend/.env)
        'feimisioPromocodesKey': '', // Дополнительный ключ безопасности промокодов (должен быть такой же как в backend/.env)
        'enotSecret': '', // Секретный ключ для оплаты через Enot
        'enotShopID': 00000, // ID магазина Enot
        'freekassaSecret': '', // Секретный ключ для оплаты через Freekassa
        'freekassaShopID': 0000, //ID магазина Freekassa
        'anypaySecret': '', // кретный ключ для оплаты через Anypay
        'anypayShopID': 0000, // ID магазина Anypay
        'siteName': 'FeimisioDonate', // Название сайта
        'titleSeparator': '–',
        'siteMetaName': 'Feimisio Donate', // Название сайта в мета-тегах
        'siteMetaDescription': 'Сервис пожертвований для вашего сервера...',
        'donateDescription': 'Пожертвования на развитие проекта Feimisio', // Описание платежа макс. 150 символов
        'siteRedirectDomain': 'https://famesrv.ru', // Основной сайт проекта
        'siteDonateDomain': 'https://donate.famesrv.ru', // Сайт доната
        'siteAPIDomain': 'https://donate.famesrv.ru', // Сайт на котором находится API системы доната
        'siteUserAgreement': 'https://famesrv.ru/custom/?id=user_agreement', // Ссылка на пользовательское соглашение
        'support': [
            {
                'title': 'VK', // Название блока
                'status': true, // Включено/выключено
                'type': 'link', // modal or link
                'icon': 'mdi:vk', // Иконка
                'href': 'https://vk.com/feimisio' // Ссылка на ваш ВК
            },
            {
                'title': 'Discord', // Название блока
                'status': true, // Включено/выключено
                'type': 'link', // modal or link
                'icon': 'simple-icons:discord', // Иконка
                'href': 'https://discord.gg/mvWQEePJAn' // Ссылка на ваш Дискорд
            },
            {
                'title': 'Telegram', // Название блока
                'status': true, // Включено/выключено
                'type': 'link', // modal or link
                'icon': 'simple-icons:telegram', // Иконка
                'href': 'https://t.me/feimisio' // Ссылка на ваш Телеграм
            },
            {
                'title': 'E-Mail', // Название блока
                'status': true, // Включено/выключено
                'type': 'modal', // modal or link
                'icon': 'mdi:email', // Иконка
                'href': 'support@famesrv.ru' // Ссылка на вашу почту
            },
            {
                'title': 'Github', // Название блока
                'status': true, // Включено/выключено
                'type': 'link', // modal or link
                'icon': 'mdi:github', // Иконка
                'href': 'https://github.com/ilyhalight/FeimisioDonate' // Ссылка на ваш Гитхаб
            }
        ]
    }
}

export default config();