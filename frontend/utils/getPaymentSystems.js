import config from '~/config/config.js';
import bestMethods from '~/config/bestMethods';
import { getTimestamp } from "~/utils/utils.js";
import { getToken } from "~/utils/getToken.js";

async function getPaymentSystems() {
  const timestamp = getTimestamp();
  const token = await getToken(timestamp);
  return await $fetch(`${config.siteAPIDomain}/api/payment-systems`, {
    method: 'GET',
    parseResponse: JSON.parse,
    headers: {
      'Authorization': `${timestamp},${token}`
    }
  });
};

function getBestPaymentMethods(paymentSystems) {
  let aggregatorsCandidates = [];
  for (let i = 0; i < bestMethods.length; i++) {
    const method = bestMethods[i];
    const preObject = {
      method: method.name,
      data: []
    }
    for (let i2nd = 0; i2nd < method.data.length; i2nd++) {
      const aggregator = method.data[i2nd];
      for (const paymentSystem of paymentSystems) {

        if (paymentSystem.name === aggregator.name && paymentSystem.disabled !== 1 && !aggregator.disabled && aggregator.commission !== undefined && aggregator.minPrice !== undefined) {
          preObject.data.push(aggregator);
        }
      }
    };
    if (preObject.data.length) aggregatorsCandidates.push(preObject);
  }

  // Sort by commission
  for (const aggregator of aggregatorsCandidates) {
    aggregator.data.sort((aggregator, aggregatorNext) => aggregator.commission - aggregatorNext.commission);
  }
  return aggregatorsCandidates;
}  

export { getPaymentSystems, getBestPaymentMethods };