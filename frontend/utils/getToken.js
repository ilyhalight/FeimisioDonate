import config from '~/config/config.js';
import shajs from 'sha.js';

async function getToken(timestamp) {
  return await shajs('sha256').update(`${config.feimisioPromocodesKey}${config.feimisioToken}${timestamp}`).digest('hex');
}

export { getToken };