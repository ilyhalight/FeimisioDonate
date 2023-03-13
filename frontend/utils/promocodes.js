import config from '~/config/config.js';
import { checkPromoCodes } from '~/utils/checkPromocodes.js';


async function checkPromoCode(promoCode, privilegeUID, t = () => {}) {
  let promoCodeError = document.getElementById('promocode_error');
  let promoCodeSuccess = document.getElementById('promocode_success');
  let donateBtn = document.getElementById('feimisio_btn');

  const promoCodeData = await checkPromoCodes(promoCode, privilegeUID);

  if (promoCodeData.data.status === true) {
    promoCodeError.control.setCustomValidity('');
    promoCodeSuccess.setAttribute('aria-hidden', 'false');
    if (promoCodeData.data.hasOwnProperty('discount')) {
      promoCodeSuccess.innerText = `${t('Promocode found')} (${t('Discount')}: ${promoCodeData.data.discount}%)`;
    } else {
      promoCodeSuccess.innerText = promoCodeData.data.msg;
    }
    
    promoCodeError.setAttribute('aria-hidden', 'true');
    donateBtn.disabled = false;
    return true;
  }

  promoCodeError.control.setCustomValidity(t('Promocode not found'));
  promoCodeError.setAttribute('aria-hidden', 'false');
  promoCodeError.innerText = t(promoCodeData.data.msg);
  promoCodeSuccess.setAttribute('aria-hidden', 'true');
  donateBtn.disabled = true;
  return false;
}

export { checkPromoCode };