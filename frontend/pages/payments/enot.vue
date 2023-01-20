<script setup>
  import { v4 as uuidv4 } from 'uuid';
  import MD5 from 'crypto-js/md5';
  const config = useRuntimeConfig();
  const enotSecret = config.public.enotSecret;
  const shopID = config.public.enotShopID;

  useHead({
    title: "Enot · Feimisio Donate",
    meta: [
      {
        name: "og:title",
        content: "Enot - Feimisio Donate"
      },
    ]
  });
</script>

<template>
  <main class="centered_container m-6 mt-2 md:mt-6">
    <div class="mx-10">
      <p class="page_title">Форма оплаты Enot</p>
      <p class="page_description">При возникновении ошибок отпишите по контактам</p>
      <form class="flex justify-center" id="enot_form" action="https://enot.io/pay" method="get">
        <input id='form-input-m' type='hidden' name='m' :value='shopID'>
        <input id='form-input-oa' type='hidden' name='oa' :value='this.price'>
        <input id='form-input-o' type='hidden' name='o' :value='this.payID'>
        <input id='form-input-s' type='hidden' name='s' :value='sign(enotSecret, shopID)'>
        <input id='form-input-cr' type='hidden' name='cr' value='RUB'>
        <input id='form-input-c' type='hidden' name='c' value='Донат на сервера Feimisio'>
        <input id='form-input-cf' type='hidden' name='cf' :value='this.uid+","+this.price+","+this.steamLink+","+this.promoCode'>
        <input id='form-input-success_url' type='hidden' name='success_url' value='http://localhost:3999/results/success'>
        <input id='form-input-fail_url' type='hidden' name='fail_url' value='http://localhost:3999/results/error'>
        <input class='donate_btn' id='form-input-submit' type="submit" value="Перейти"/>
      </form>
    </div>
  </main>
</template>

<script>
  export default {
    data() {
      return {
        uid: 0,
        price: 10000000,
        steamLink: '',
        payID: '',
        promoCode: ''
      };
    },

    created: async function() {
      this.payID = uuidv4();
      if (process.client) {
        const windowData = Object.fromEntries(
          new URL(window.location).searchParams.entries()
        );

        if (windowData.uid) {
          this.uid = windowData.uid;
        }

        if (windowData.price) {
          this.price = windowData.price;
        }

        if (windowData.steam) {
          this.steamLink = windowData.steam;
        }

        if (windowData.promocode) {
          this.promoCode = windowData.promocode;
        }

        if (this.uid > 0) {
          const data = await $fetch(`http://localhost:3312/api/privillege?uid=${this.uid}`);
          if (data) {
            if (data.discount > 0 && data.price > 0) {
              this.price = Math.round(data.price - (data.price / 100 * data.discount))
            } else {
              this.price = data.price;
            }
          }
        }
        let form = document.getElementById('enot_form');
        form.submit();
      }
    },

    methods: {
      uuidv4() {
        return uuidv4();
      },
      sign(secret, shopID) {
        return MD5(shopID.toString() + ':' + this.price + ':' + secret.toString() + ':' + this.payID)
      }
    }
  }
</script>