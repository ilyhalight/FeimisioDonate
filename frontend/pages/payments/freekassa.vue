<script setup>
  import { v4 as uuidv4 } from 'uuid';
  import MD5 from 'crypto-js/md5';

  useHead({
    title: "Freekassa · Feimisio Donate",
    meta: [
      {
        name: "og:title",
        content: "Freekassa - Feimisio Donate"
      },
    ]
  });

  const config = useRuntimeConfig();
  const freekassaSecret = config.public.freekassaSecret;
  const shopID = config.public.freekassaShopID;
</script>

<template>
  <main class="centered_container m-6 mt-2 md:mt-6">
    <div class="mx-10">
      <p class="page_title">Форма оплаты Freekassa</p>
      <p class="page_description">При возникновении ошибок отпишите по контактам</p>
      <form class="flex justify-center" id="freekassa_form" action="https://pay.freekassa.ru/" method="get">
        <input id='form-input-m' type='hidden' name='m' :value='shopID'>
        <input id='form-input-oa' type='hidden' name='oa' :value='this.price'>
        <input id='form-input-o' type='hidden' name='o' :value='this.payID'>
        <input id='form-input-s' type='hidden' name='s' :value='sign(freekassaSecret, shopID)'>
        <input id='form-input-currency' type='hidden' name='currency' value='RUB'>
        <input id='form-input-i' type='hidden' name='i' value='1'>
        <input id='form-input-lang' type='hidden' name='lang' value='ru'>
        <input id='form-input-us' type='hidden' name='us_uid' :value='this.uid'>
        <input id='form-input-us' type='hidden' name='us_price' :value='this.price'>
        <input id='form-input-us' type='hidden' name='us_steamLink' :value='this.steamLink'>
        <input id='form-input-us' type='hidden' name='us_promoCode' :value='this.promoCode'>
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
          const data = await $fetch(`http://localhost:3999/api/privillege?uid=${this.uid}`);
          if (data) {
            if (data.discount > 0 && data.price > 0) {
              this.price = Math.round(data.price - (data.price / 100 * data.discount))
            } else {
              this.price = data.price;
            }
          }
        }
        let form = document.getElementById('freekassa_form');
        form.submit();
      }
    },

    methods: {
      uuidv4() {
        return uuidv4();
      },
      sign(secret, shopID) {
        return MD5(shopID.toString() + ':' + this.price + ':' + secret.toString() + ':' + 'RUB' + ':' + this.payID)
      }
    }
  }
</script>