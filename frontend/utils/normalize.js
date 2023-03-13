function normalizePrice(price, discount, t = () => {}) {
  if (price === 0) {
    return t('Free');
  } else {
    if (discount === 0) {
      return `${price}₽`;
    } else {
      return `${Math.round(price - (price / 100 * discount))}₽`;
    }
  }
}

function normalizeDuration(duration, t = () => {}) {
  if (duration === 0) {
    return t('forever');
  } else if (duration % 24 === 0) {
    return `${duration / 24} ${t('d')}.`;
  } else {
    return `${duration} ${t('hour')}.`;
  }
}

function getFinalPrice(price, discount, t = () => {}) {
  let priceNormalized = normalizePrice(price, discount, t);
  if (discount > 0 && price > 0) {
    return `<span style="text-decoration: line-through;">${price}₽</span><span style="color: red">${priceNormalized}</span>`;
  } else {
    return priceNormalized;
  }
}

export { normalizePrice, normalizeDuration, getFinalPrice }; 