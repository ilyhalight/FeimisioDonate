<script setup>
  import { getTimestamp } from '~/utils/utils.js';
  import config from '~/config/config.js';
  import { signMD5v2 } from '~/utils/sign.js';
  import { getPrivilegeByUID } from '~/utils/getPrivileges.js';

  const route = useRoute();
  const { t } = useI18n();

  definePageMeta({
    title: 'AnyPay'
  });

  useHead({
    meta: [
      {
        name: "description",
        content: `${t('Paying for a privilege with')} AnyPay`
      },
    ]
  });

  const anypaySecret = config.anypaySecret;
  const shopID = config.anypayShopID;

  const uid = ref(0);
  const price = ref(10000000);
  const steamLink = ref('');
  const payID = ref(0);
  const currency = ref('RUB');
  const promoCode = ref('');

  payID.value = getTimestamp();

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
  const signature = signMD5v2(currency.value, price.value, anypaySecret, shopID, payID.value).toString();

  onMounted(() => {
    let form = document.getElementById('anypay_form');
    form.submit();
  });
</script>

<template>
  <main class="wrapper">
    <div>
      <p class="text-attractive">{{ $t('Form of payment')}} AnyPay</p>
      <p class="subtext-attractive">{{ $t('If you encounter any errors, write to support') }}</p>
      <form id="anypay_form" action="https://anypay.io/merchant" method="get">
        <input type='hidden' name='merchant_id' :value='shopID'>
        <input type='hidden' name='pay_id' :value='payID'>
        <input type='hidden' name='amount' :value='price'>
        <input type='hidden' name='currency' :value='currency'>
        <input type='hidden' name='desc' :value='config.donateDescription'>
        <input type='hidden' name='success_url' :value="config.siteDonateDomain+'/results/success'">
        <input type='hidden' name='fail_url' :value="config.siteDonateDomain+'/results/error'">
        <input type='hidden' name='sign' :value='signature'>
        <input type='hidden' name='field1' :value='field1'>
        <input class='button' type="submit" :value="$t('Purchase')"/>
      </form>
    </div>
  </main>
</template>