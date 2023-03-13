import MD5 from 'crypto-js/md5';

function signMD5v2(currency, price, secret, shopID, payID) {
    return MD5(`${currency}:${price}:${secret}:${shopID}:${payID}`);
}

function signMD5v1(shopID, price, secret, payID) {
    return MD5(`${shopID}:${price}:${secret}:${payID}`);
}

export { signMD5v2, signMD5v1 };