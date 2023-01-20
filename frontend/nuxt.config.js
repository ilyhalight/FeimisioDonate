import fs from 'fs';

export default defineNuxtConfig({
    modules: [
        '@nuxtjs/tailwindcss',
        '@nuxtjs/color-mode'
    ],
    css: [
        '~/assets/css/main.css',
    ],
    tailwindcss: {
        exposeConfig: true
    },
    colorMode: {
        preference: 'system', // default theme
        dataValue: 'theme', // activate data-theme in <html> tag
        classSuffix: '',
    },
    app: {
        head: {
            title: 'Главная · Feimisio Donate',
            meta: [
                { charset: 'utf-8' },
                { name: 'viewport', content: 'width=device-width, initial-scale=1' },
                { name: 'description', content: 'Feimisio Donate - Сервис пожертвований для вашего сервера' },
                { name: 'og:description', content: 'Feimisio Donate - Сервис пожертвований для вашего сервера' },
                { name: 'keywords', content: 'feimisio, feimisiodonate, donate, feimisio_donate, csgo, server, fame server, famesrv, minecraft, feimisio discord, feimisio site' },
                { name: 'og:locale', content: 'ru_RU' },
                { name: 'og:type', content: 'website' },
                { name: 'og:title', content: 'Главная - Feimisio Donate' },
                { name: 'og:site_name' },
                { name: 'og:image', content: '/favicon.svg'}
            ],
            link: [
                { rel: 'icon', type: 'image/svg', href: '/favicon.svg' }
            ]
        }
    },
    // vite: {
    //     server: {
    //         https: {
    //             key: fs.readFileSync('/etc/letsencrypt/live/toiloff.ru/privkey.pem'),
    //             cert: fs.readFileSync('/etc/letsencrypt/live/toiloff.ru/fullchain.pem'),
    //         },
    //         hmr: {
    //             protocol: 'wss',
    //         }
    //     }
    // },
    runtimeConfig: {
        public: {
            enotSecret: process.env.ENOT_SECRET,
            enotShopID: process.env.ENOT_SHOPID,
            freekassaSecret: process.env.FREEKASSA_SECRET,
            freekassaShopID: process.env.FREEKASSA_SHOPID,
        },
    },
    env: {
        baseUrl: `http://0.0.0.0:${process.env.PORT}` || 'http://localhost:3000',
    },
    debug: false,
})