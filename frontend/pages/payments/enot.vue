<script setup>
  import { v4 as uuidv4 } from 'uuid';
  import config from '~/config/config.js';
  import { signMD5v1 } from '~/utils/sign.js';
  import { getPrivilegeByUID } from '~/utils/getPrivileges.js';

  const route = useRoute();
  const { t } = useI18n();

  definePageMeta({
    title: 'Enot'
  });

  useHead({
    meta: [
      {
        name: "description",
        content: `${t('Paying for a privilege with')} Enot`
      },
    ]
  });

  const enotSecret = config.enotSecret;
  const shopID = config.enotShopID;

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

  const field1 = `${uid.value}, ${price.value}, ${steamLink.value}, ${promoCode.value}`;

  onMounted(() => {
    let form = document.getElementById('enot_form');
    form.submit();
  });
</script>


<template>
  <main class="wrapper">
    <div>
      <p class="text-attractive">{{ $t('Form of payment')}} Enot</p>
      <p class="subtext-attractive">{{ $t('If you encounter any errors, write to support') }}</p>
      <form id="enot_form" action="https://enot.io/pay" method="get">
        <input id='form-input-m' type='hidden' name='m' :value='shopID'>
        <input id='form-input-oa' type='hidden' name='oa' :value='price'>
        <input id='form-input-o' type='hidden' name='o' :value='payID'>
        <input id='form-input-s' type='hidden' name='s' :value='signMD5v1(shopID, price, enotSecret, payID)'>
        <input id='form-input-cr' type='hidden' name='cr' :value='currency'>
        <input id='form-input-c' type='hidden' name='c' :value='config.donateDescription'>
        <input id='form-input-cf' type='hidden' name='cf' :value='field1'>
        <input id='form-input-success_url' type='hidden' name='success_url' :value="config.siteDonateDomain+'/results/success'">
        <input id='form-input-fail_url' type='hidden' name='fail_url' :value="config.siteDonateDomain+'/results/error'">
        <input class='button' id='form-input-submit' type="submit" :value="$t('Purchase')"/>
      </form>
    </div>
  </main>
</template>