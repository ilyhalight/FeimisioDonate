import { checkPromoCode } from "~/utils/promocodes.js";

const STEAM_REGEX = /^(https:\/\/|http:\/\/)?steamcommunity.com\/(id|profiles)\/.+$/;


async function checkSteamLink(steamLink, t = () => {}) {
  let donateBtn = document.getElementById('feimisio_btn');
  let steamLinkError = document.getElementById('steam_link_error');
  if (steamLink && STEAM_REGEX.test(steamLink) && !steamLink.includes(' ')) {
    steamLinkError.control.setCustomValidity('');
    steamLinkError.setAttribute('aria-hidden', 'true');
    donateBtn.disabled = false;
    return true;
  } else if (steamLink) {
    steamLinkError.control.setCustomValidity(t('Link not valid'));
    steamLinkError.textContent = t('Link not valid');
    steamLinkError.setAttribute('aria-hidden', 'false');
    donateBtn.disabled = true;
  } else {
    steamLinkError.control.setCustomValidity(t('Link not entered'));
    steamLinkError.textContent = t('Link not entered');
    steamLinkError.setAttribute('aria-hidden', 'false');
    donateBtn.disabled = true;
  }
  return false;
}

async function checkSteamAndPromo(privillegeUID, t = () => {}) {
  let steamLink = document.getElementById('steam_link').value;
  let promo = document.getElementById('promocode').value;
  const steamResult = await checkSteamLink(steamLink, t);
  const promoCodeResult = await checkPromoCode(promo, privillegeUID, t);
  if (steamResult && promoCodeResult) {
    document.getElementById('feimisio_btn').disabled = false;
  } else {
    document.getElementById('feimisio_btn').disabled = true;
  }
}

export { checkSteamAndPromo };