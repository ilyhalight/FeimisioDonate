<script setup>
  import config from '~/config/config.js';
  import { checkSteamAndPromo } from '~/utils/checkSteam.js';
  import { getPaymentSystems, getBestPaymentMethods } from '~/utils/getPaymentSystems.js';
  import Accordion from '~/components/Accordion.vue';

  const props = defineProps({
    selected: {
      type: Object,
      required: true,
    },
  });

  const { t } = useI18n();

  const steamLink = ref('');
  const promoCode = ref('');
  const bestPaymentMethods = ref([]);
  const selectedMethod = ref('');

  const paymentSystems = await useAsyncData(async () => {
    return await getPaymentSystems();
  });

  if (paymentSystems?.data?.value?.length) {
    bestPaymentMethods.value = getBestPaymentMethods(paymentSystems.data.value);
  }

  watch(steamLink, async () => await checkSteamAndPromo(props.selected.uid, t));

  watch(promoCode, async () => await checkSteamAndPromo(props.selected.uid, t));

  function clearMethods(methods) {
    for (let aggregator of methods) {
      if (aggregator.data && aggregator.data.length) {
        const method = aggregator.data.filter((method) => method.minPrice <= props.selected.price);
        if (!method.length) {
          methods.splice(methods.indexOf(aggregator), 1)
          continue;
        }

        aggregator.data = [];
        for (let i = 0; i < method.length; i++) {
          aggregator.data.push(method[i]);
        }
      }
    }
    return methods;
  }

  const availableMethods = computed(() => {
    for (let i = 0; i < bestPaymentMethods.value.length; i++) {
      bestPaymentMethods.value = clearMethods(bestPaymentMethods.value);
    }

    return bestPaymentMethods.value
  });

  function getSelectedMethod() {
    for (let aggregator of availableMethods.value) {
      selectedMethod.value = `${aggregator.data[0].name};${aggregator.method}`;
      return selectedMethod.value;
    }
  };

  getSelectedMethod();

  watch(selectedMethod, () => {
    let methodBtns = document.getElementById('payment-systems').children;
    for (let i = 0; i < methodBtns.length; i++) {
      methodBtns[i].setAttribute('aria-checked', 'false');
    }
    document.getElementById(selectedMethod.value.split(';')[1]).setAttribute('aria-checked', 'true');
    document.getElementsByName('selectedMethod')[0].setAttribute('value', selectedMethod.value);
  });

</script>

<template>
  <form method="post" :action="config.siteAPIDomain+ '/api/payments-methods'">
    <div class="donate-form" v-if="bestPaymentMethods.length">
      <div class="input-box">
        <label for="steam_link" role="text">
          {{ $t('Enter the link to') }} <a class="text-gradient" href="https://steamcommunity.com/">Steam</a> {{ $t('profile') }}
        </label>
        <input v-model="steamLink" id="steam_link" name="steam_link" type="url" placeholder="https://steamcommunity.com/id/EXAMPLE" autocomplete="on">
        <label class="error" id="steam_link_error" for="steam_link" aria-hidden="true" role="text">
          {{ $t('Link not entered') }}
        </label>
      </div>
      <input type="hidden" :value="selected.uid" name="uid">
      <input type="hidden" :value="selectedMethod" name="selectedMethod">
      <div class="input-box">
        <label for="promocode" role="text">
          {{ $t('Enter the promo code (if available)') }}
        </label>
        <input v-model="promoCode" id="promocode" name="promocode" type="text" :placeholder="$t('Promocode')" autocomplete="off">
        <label class="error" id="promocode_error" for="promocode" aria-hidden="true" role="text">
          {{ $t('Promocode not found') }}
        </label>
        <label class="success" id="promocode_success" for="promocode" aria-hidden="true" role="text">
          {{ $t('Promocode found') }}
        </label>
      </div>
      <div class="payments">
        <p>{{ $t('Choose a payment system') }}</p>
        <div class="payment-systems" id="payment-systems" v-if="paymentSystems.data.value.length || selected.price == 0">
          <template v-if="selected.price == 0">
            <div class="payment-system" id="gift" @click="selectedMethod = 'gift'" :aria-checked="selected.price == 0 ? 'true' : ''">
              <nuxt-img src="/images/methods/gift.png" alt="gift" width="100" height="36"/>
            </div>
          </template>
          <template v-if="selected.price != 0 && availableMethods.length"> 
            <div v-for="paymentMethod of availableMethods" :key="paymentMethod.method" :aria-roledescription="paymentMethod.data[0].name" class="payment-system" :id="paymentMethod.method" @click="selectedMethod = `${paymentMethod.data[0].name};${paymentMethod.method}`" :aria-checked="paymentMethod.method === selectedMethod.split(';')[1] ? 'true' : 'false'">
              <nuxt-img :src="`/images/methods/${paymentMethod.method}.svg`" :alt="paymentMethod.method" width="100" height="48"/>
            </div>
          </template>
        </div>
        <div v-else>
          <p class="error">{{ $t('The administrator did not indicate the available payment systems. Purchase is not possible') }}!</p>
        </div>
      </div>
      <div class="action-btn">
        <input type="submit" id="feimisio_btn" class="button" value="Приобрести" disabled>
      </div>
    </div>
    <div class="donate-form-error" v-else>
      <div class="texts">
        <h3 class="title error">{{ $t('API Error')+'!' }}</h3>
        <p class="description error">{{ $t('Could not get information about available payment systems. Inform the administration about the error. Purchase is not possible.') }}</p>
        <Accordion :title="$t('Possible solution')">
          <template #content>
            <p>{{ $t('Compare your time with the time on the site time.is . If your watch is more than 30 seconds behind, then you will not be able to interact with our site.') }}</p>
          </template>
        </Accordion>
      </div>
    </div>
  </form>
</template>