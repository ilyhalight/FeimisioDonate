<script setup>
  import { v4 as uuidv4 } from 'uuid';
  import config from '~/config/config.js';
  import { signMD5v2 } from '~/utils/sign.js';
  import { getPrivilegeByUID } from '~/utils/getPrivileges.js';

  const route = useRoute();
  const { t } = useI18n();

  definePageMeta({
    title: 'Freekassa'
  });

  useHead({
    meta: [
      {
        name: "description",
        content: `${t('Paying for a privilege with')} Freekassa`
      },
    ]
  });

  const freekassaSecret = config.freekassaSecret;
  const shopID = config.freekassaShopID;

  const uid = ref(0);
  const price = ref(10000000);
  const steamLink = ref('');
  const payID = ref(0);
  const currency = ref('RUB');
  const promoCode = ref('');

  payID.value = uuidv4(); 

  uid.value = route.query.uid;
  price.value = route.query.price;
  steamLink.value = route.query.steam;
  currency.value = route.query.currency;
  promoCode.value = route.query.promocode;

  if (uid.value > 0) {
    const data = await getPrivilegeByUID(uid.value);
    if (data) {
      if (data.discount > 0 && data.price > 0) {
        price.value = Math.round(data.price - (data.price / 100 * data.discount))
      } else {
        price.value = data.price;
      }
    }
  }

  onMounted(() => {
    let form = document.getElementById('freekassa_form');
    form.submit();
  });
</script>



<template>
  <main class="wrapper">
    <div>
      <p class="text-attractive">{{ $t('Form of payment')}} Freekassa</p>
      <p class="subtext-attractive">{{ $t('If you encounter any errors, write to support') }}</p>
      <form id="freekassa_form" action="https://pay.freekassa.ru/" method="get">
        <input id='form-input-m' type='hidden' name='m' :value='shopID'>
        <input id='form-input-oa' type='hidden' name='oa' :value='price'>
        <input id='form-input-o' type='hidden' name='o' :value='payID'>
        <input id='form-input-s' type='hidden' name='s' :value='signMD5v2(shopID, price, freekassaSecret, currency, payID)'>
        <input id='form-input-currency' type='hidden' name='currency' :value='currency'>
        <input id='form-input-i' type='hidden' name='i' value='1'>
        <input id='form-input-lang' type='hidden' name='lang' value='ru'>
        <input id='form-input-us' type='hidden' name='us_uid' :value='uid'>
        <input id='form-input-us' type='hidden' name='us_price' :value='price'>
        <input id='form-input-us' type='hidden' name='us_steamLink' :value='steamLink'>
        <input id='form-input-us' type='hidden' name='us_promoCode' :value='promoCode'>
        <input class='button' id='form-input-submit' type="submit" :value="$t('Purchase')"/>
      </form>
    </div>
  </main>
</template>