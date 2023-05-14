import config from '~/config/config.js';
import { getTimestamp } from "~/utils/utils.js";
import { getToken } from "~/utils/getToken.js";

async function checkPromoCodes(promoCode, privilegeUID) {
  const timestamp = getTimestamp();
  const token = await getToken(timestamp);

  return await $fetch(`${config.siteAPIDomain}/api/promocodes/check`, {
    method: 'POST',
    parseResponse: JSON.parse,
    headers: {
      'Authorization': `${timestamp},${token}`
    },
    query: {
      privilege: privilegeUID,
      promo: promoCode
    },
    server: false,
  });
};

export { checkPromoCodes };