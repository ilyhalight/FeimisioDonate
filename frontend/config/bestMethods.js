const bestAggregators = () => {
    const USD_PRICE = 75;
    const UNDEFINED_PRICE = 100;
    return [
        {
            name: 'qiwi',
            data: [
                {
                    name: 'enot',
                    minPrice: undefined,
                    commission: 3.5,
                    disabled: true
                },
                {
                    name: 'anypay',
                    minPrice: 10,
                    commission: 6.9,
                    disabled: false
                },
                {
                    name: 'freekassa',
                    minPrice: 10,
                    commission: 5.0,
                    disabled: false
                },
                {
                    name: 'lava',
                    minPrice: 10,
                    commission: 2.5, // 2.5% you - 2.5% client, edit if you edit this in dashboard
                    disabled: false
                }
            ]
        },
        {
            name: 'ru_cards',
            data: [
                {
                    name: 'enot',
                    minPrice: 100,
                    commission: 3.0,
                    disabled: false
                },
                {
                    name: 'crystalpay',
                    minPrice: 500,
                    commission: 2.5,
                    disabled: true // needed professional status
                },
                {
                    name: 'anypay',
                    minPrice: 10,
                    commission: 6.9,
                    disabled: false
                },
                {
                    name: 'freekassa',
                    minPrice: 10,
                    commission: 2.8,
                    disabled: false
                },
                {
                    name: 'lava',
                    minPrice: 10,
                    commission: 2.5, // 2.5% you - 2.5% client, edit if you edit this in dashboard
                    disabled: false
                },
                {
                    name: 'paypalych',
                    minPrice: 15,
                    commission: 8.0,
                    disabled: false
                },
            ]
        },
        {
            name: 'another_cards',
            data: [
                {
                    name: 'enot',
                    minPrice: 10,
                    commission: 3.0,
                    disabled: false
                },
                {
                    name: 'freekassa',
                    minPrice: 10,
                    commission: 7.0,
                    disabled: false
                },
                {
                    name: 'paypalych',
                    minPrice: USD_PRICE,
                    commission: 8.0,
                    disabled: false
                },
            ]
        },
        {
            name: 'yoomoney',
            data: [
                {
                    name: 'enot',
                    minPrice: 10,
                    commission: 5.0,
                    disabled: false
                },
                {
                    name: 'anypay',
                    minPrice: 10,
                    commission: 6.5,
                    disabled: false
                },
                {
                    name: 'freekassa',
                    minPrice: 300,
                    commission: 5.0,
                    disabled: false
                },
            ]
        },
        {
            name: 'perfectmoney',
            data: [
                {
                    name: 'enot',
                    minPrice: 10,
                    commission: 2.5,
                    disabled: false
                },
                {
                    name: 'anypay',
                    minPrice: 1,
                    commission: 2.0,
                    disabled: false
                },
                {
                    name: 'freekassa',
                    minPrice: USD_PRICE,
                    commission: 5.0,
                    disabled: false
                },
            ]
        },
        {
            name: 'lolzteam',
            data: [
                {
                    name: 'crystalpay',
                    minPrice: 1,
                    commission: 1.0,
                    disabled: false
                },
            ]
        },
        {
            name: 'crystalpay',
            data: [
                {
                    name: 'crystalpay',
                    minPrice: 1,
                    commission: 0.0,
                    disabled: false
                },
            ]
        },
        {
            name: 'lava',
            data: [
                {
                    name: 'lava',
                    minPrice: 1,
                    commission: 0.0, // 2.5% you - 2.5% client, edit if you edit this in dashboard
                    disabled: false
                }
            ]
        },
        {
            name: 'advcashwallet',
            data: [
                {
                    name: 'anypay',
                    minPrice: 1,
                    commission: 2.0,
                    disabled: false
                },
            ]
        },
        {
            name: 'webmoney',
            data: [
                {
                    name: 'anypay',
                    minPrice: undefined,
                    commission: undefined,
                    disabled: true
                },
                {
                    name: 'freekassa',
                    minPrice: USD_PRICE,
                    commission: 3.0,
                    disabled: true
                },
            ]
        },
        {
            name: 'megafon',
            data: [
                {
                    name: 'anypay',
                    minPrice: 10,
                    commission: 5.0,
                    disabled: false
                },
                {
                    name: 'freekassa',
                    minPrice: UNDEFINED_PRICE,
                    commission: 7.0,
                    disabled: false
                },
            ]
        },
        {
            name: 'beeline',
            data: [
                {
                    name: 'freekassa',
                    minPrice: UNDEFINED_PRICE,
                    commission: 7.0,
                    disabled: false
                },
            ]
        },
        {
            name: 'mts',
            data: [
                {
                    name: 'freekassa',
                    minPrice: UNDEFINED_PRICE,
                    commission: 7.0,
                    disabled: false
                },
            ]
        },
        {
            name: 'tele2',
            data: [
                {
                    name: 'freekassa',
                    minPrice: UNDEFINED_PRICE,
                    commission: 7.0,
                    disabled: false
                },
            ]
        },
        {
            name: 'fkwallet',
            data: [
                {
                    name: 'freekassa',
                    minPrice: 10,
                    commission: 3.0,
                    disabled: false
                },
            ]
        },
        {
            name: 'steamskins',
            data: [
                {
                    name: 'freekassa',
                    minPrice: 50,
                    commission: 3.0,
                    disabled: false
                },
            ]
        },
        {
            name: 'sbp',
            data: [
                {
                    name: 'freekassa',
                    minPrice: 10,
                    commission: 2.0,
                    disabled: false
                },
            ]
        },
        {
            name: 'cryptoanypay',
            data: [
                {
                    name: 'crystalpay',
                    minPrice: 100,
                    commission: 0.0,
                    disabled: false
                },
            ]
        },
        {
            name: 'cryptoenot',
            data: [
                {
                    name: 'enot',
                    minPrice: 10,
                    commission: 2.0,
                    disabled: false
                },
            ]
        },
        {
            name: 'cryptocrystalpay',
            data: [
                {
                    name: 'crystalpay',
                    minPrice: 100,
                    commission: 3.0,
                    disabled: false
                },
            ]
        },
        {
            name: 'cryptofreekassa',
            data: [
                {
                    name: 'freekassa',
                    minPrice: 100,
                    commission: 0.5,
                    disabled: false
                },
            ]
        },
    ]
}

export default bestAggregators();