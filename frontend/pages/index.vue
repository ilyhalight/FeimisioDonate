<script setup>
  import BlockLoading from "~/components/donate/BlockLoading.vue";
  import VTailwindModal from "~/components/VTailwindModal.vue";
  import shajs from 'sha.js';
  import config from '~/config/config.js';

  useHead({
    title: "Главная · Feimisio Donate",
    meta: [
      {
        name: "og:title",
        content: "Главная - Feimisio Donate"
      },
    ],
  });

  function getTimestamp() {
    return Math.floor(Date.now() / 1000)
  }

  async function getToken(timestamp) {
    const token = await shajs('sha256').update(`${config.feimisioPromocodesKey}${config.feimisioToken}${timestamp}`).digest('hex');
    return token
  }

  const donateList = await useAsyncData(async () => {
    const response = await $fetch('http://127.0.0.1:3312/api/privilleges');
    return response;
  });
  const promoCodeList = await useAsyncData(async () => {
    const timestamp = getTimestamp();
    const token = await getToken(timestamp);
    const response = await $fetch('http://127.0.0.1:3312/api/promocodes', {
      headers: {
        'Authorization': `${timestamp},${token}`
      },
    });
    return response;
  })
  const selectedAggregator = ref('freekassa');
  const steamLink = ref('');
  const promoCode = ref('');
  const promoCodeDiscount = ref(0);
  const modalShow = ref(false);
  const previousPrice = ref(0);
  const selected = ref({
    uid: 1,
    name: 'VIP',
    price: 10000
  });

  function normalizePrice(price, discount) {
    if (price === 0) {
      return "Бесплатно";
    } else {
      if (discount === 0) {
        return `${price}₽`;
      } else {
        return `${Math.round(price - (price / 100 * discount))}₽`
      }
    }
  }

  function normalizeDuration(duration) {
    if (duration === 0) {
      return 'навсегда';
    } else if (duration % 24 === 0 && duration / 24 % 30 === 0) {
      return `${duration / 24 / 30 === 1 ? '' : `${duration / 24 / 30} `}мес.`;
    } else if (duration % 24 === 0) {
      return `${duration / 24} дн`;
    } else {
      return `${duration} час.`;
    }
  }

  function getFinalPrice(duration, price, discount) {
    let priceNormalized = normalizePrice(price, discount);
    let durationNormalized = normalizeDuration(duration);
    let durationBlock = `<small class="donate_expire">/${durationNormalized}</small>`
    if (discount > 0 && price > 0) {
      return `<span class="line-through">${price}₽${durationBlock}</span><br> <span class="text-red-400">${priceNormalized}${durationBlock}</span>`;
    } else {
      return `${priceNormalized}${durationBlock}`;
    }
  }

  function cancelModal(close) {
    modalShow.value = false;
  }

  function confirmModal() {
    let steamLink = document.getElementById('steam_link').value;
    let steamLinkError = document.getElementById('steam_link_error');
    if (steamLink && /^(https:\/\/|http:\/\/)?steamcommunity.com\/(id|profiles)\/.*$/.test(steamLink)) {
      modalShow.value = false;
    } else if (steamLink) {
      steamLinkError.textContent = 'Ссылка не валидна';
      steamLinkError.classList.remove('hidden');
    } else {
      steamLinkError.textContent = 'Ссылка не введена';
      steamLinkError.classList.remove('hidden');
    }
  }

  async function checkPromoCode(promoCode) {
    let promoCodeError = document.getElementById('promocode_error');
    let promoCodeSuccess = document.getElementById('promocode_success');
    let donateBtn = document.getElementById('feimisio_btn');
    // let promoCodeInput = document.getElementById('promocode');
    // promoCodeInput.value = promoCode;
    if (promoCode === '') {
      promoCodeError.classList.add('hidden');
      promoCodeSuccess.classList.add('hidden');
      donateBtn.disabled = false;
      selected.value.price = previousPrice.value;
      return true;
    }
    for (let i = 0; i < promoCodeList.data.value.length; i++) {
      let currentPromo = promoCodeList.data.value[i];
      if (currentPromo.key == promoCode) {
        if (selected.value.price <= currentPromo.min_price || selected.value.price > currentPromo.max_price) {
          donateBtn.disabled = true;
          promoCodeError.classList.remove('hidden');
          promoCodeError.innerText = 'Промокод не может быть применен к этой привилегии';
          promoCodeSuccess.classList.add('hidden');
          selected.value.price = previousPrice.value;
          return false;
        } else {
          const timestamp = getTimestamp();
          const token = await getToken(timestamp);
          const promoCodeUsagesData = await $fetch(`http://127.0.0.1:3312/api/promocodes/uses?promo=${currentPromo.key}`, {
            headers: {
              'Authorization': `${timestamp},${token}`
            },
          });
          // const promoCodeUsagesData = promoCodeUsesList.data.value.filter(promo => promo.key === promoCode);
          if (promoCodeUsagesData.length >= currentPromo.uses) {
            donateBtn.disabled = true;
            promoCodeError.innerText = 'Превышено количество использований этого промокода';
            promoCodeError.classList.remove('hidden');
            promoCodeSuccess.classList.add('hidden');
            selected.value.price = previousPrice.value;
            return false;
          } else {
            promoCodeDiscount.value = currentPromo.discount;
            if (currentPromo.discount === 100) {
              if (selected.value.price !== 0) {
                previousPrice.value = selected.value.price;
              }
              selected.value.price = 0;
            } else {
              selected.value.price = previousPrice.value;
            }
            promoCodeError.classList.add('hidden');
            promoCodeSuccess.classList.remove('hidden');
            donateBtn.disabled = false;
            return true;
          }
        }
      } else {
        donateBtn.disabled = true;
        promoCodeError.classList.remove('hidden');
        promoCodeError.innerText = 'Промокод не найден';
        promoCodeSuccess.classList.add('hidden');
        selected.value.price = previousPrice.value;
      }
    }
    return false;
  }

  async function checkSteamLink(steamLink) {
    let donateBtn = document.getElementById('feimisio_btn');
    let steamLinkError = document.getElementById('steam_link_error');
    if (steamLink && /^(https:\/\/|http:\/\/)?steamcommunity.com\/(id|profiles)\/.*$/.test(steamLink)) {
      steamLinkError.classList.add('hidden');
      donateBtn.disabled = false;
      return true;
    } else if (steamLink) {
      steamLinkError.textContent = 'Ссылка не валидна';
      steamLinkError.classList.remove('hidden');
      donateBtn.disabled = true;
    } else {
      steamLinkError.textContent = 'Ссылка не введена';
      steamLinkError.classList.remove('hidden');
      donateBtn.disabled = true;
    }
    return false;
  }

  async function checkSteamAndPromo() {
    let steamLink = document.getElementById('steam_link').value;
    let promo = document.getElementById('promocode').value;
    const steamResult = await checkSteamLink(steamLink);
    const promoCodeResult = await checkPromoCode(promo);
    if (steamResult && promoCodeResult) {
      document.getElementById('feimisio_btn').disabled = false;
    } else {
      document.getElementById('feimisio_btn').disabled = true;
    }
  }

  watch(selectedAggregator, () => {
    let aggregatorBtns = document.getElementById('aggregators').children;
    for (let i = 0; i < aggregatorBtns.length; i++) {
      aggregatorBtns[i].classList.remove('active');
    }
    document.getElementById(selectedAggregator.value).classList.add('active');
  });

  watch(steamLink, checkSteamAndPromo);

  watch(promoCode, checkSteamAndPromo);
</script>

<template>
    <main class="centered_container m-6 mt-2 md:mt-6">
      <p class="page_title">Донат</p>
      <section class="donate_section">
          <template v-if="donateList.data.value.length">
            <div v-for="donate in donateList.data.value" :key="donate.uid" class="donate_block">
              <p class="donate_title">{{ donate.name }}</p>
              <p class="donate_price" v-html="getFinalPrice(donate.duration, donate.price, donate.discount)"></p>
              <div class="text-xl mt-4 mb-4">Вы получите доступ к:
                  <ul class="donate_features">
                    <li v-for="feature in donate.short_description.split(';')" :key="feature">{{ feature }}</li>
                  </ul>   
                  <NuxtLink class="donate_link" :bind="donate.link" :to="'/info/'+donate.link" target="_blank">Подробнее...</NuxtLink>
              </div>
              <label :key="donate.uid" :id="'buy_'+donate.uid" class="feimisio_btn" @click="selected.uid = donate.uid; selected.name = donate.name; selected.price = donate.price; previousPrice = donate.price; promoCode = ''; modalShow = true">Приобрести</label>
            </div>
          </template>
          <template v-else>
            <BlockLoading/>
            <BlockLoading/>
            <BlockLoading/>
            <BlockLoading/>
            <BlockLoading/>
            <BlockLoading/>
            <BlockLoading/>
            <BlockLoading/>
            <BlockLoading/>
          </template>
      </section>
      <div>
        <v-tailwind-modal v-model="modalShow" @cancel="cancelModal">
          <form class="-mt-2" method="post" action="http://127.0.0.1:3312/api/payments-methods">
            <p class="text-center text-xl font-bold">Покупка {{ selected.name }}</p>
            <div class="mt-4">
              <label class="block mb-2" for="steam_link">
                Введите ссылку на <a class="donate_link" href="https://steamcommunity.com/">Steam</a> профиль:
              </label>
              <label class="text-error hidden" id="steam_link_error" for="steam_link">
                Ссылка не введена
              </label>
              <input v-model="steamLink" class="text_input" id="steam_link" name="steam_link" type="url" placeholder="https://steamcommunity.com/id/EXAMPLE" autocomplete="on" required>
              <input type="hidden" :value="selected.uid" name="uid">
              <input type="hidden" :value="selectedAggregator" name="aggregator">
              <label class="block mb-2 mt-4" for="promocode">
                Введите промокод (если есть)
              </label>
              <label class="text-error hidden" id="promocode_error" for="promocode">
                Промокод не найден
              </label>
              <label class="text-success hidden" id="promocode_success" for="promocode">
                Промокод найден (Скидка: {{ promoCodeDiscount }}%)
              </label>
              <input v-model="promoCode" class="text_input" id="promocode" name="promocode" type="text" placeholder="Промокод" autocomplete="off">
              <p class="block mt-4">Выберите платежную систему:</p>
              <div class="flex flex-wrap justify-between" id="aggregators">
                <div v-if="selected.price == 0" class="aggregator_btn" :class="selected.price == 0 ? 'active' : ''" id="gift" @click="selectedAggregator = 'gift'">
                  <img src="~/assets/images/aggregators/gift.png" alt="gift" width="100" height="32">
                </div>
                <div v-if="selected.price != 0" class="aggregator_btn active" id="freekassa" @click="selectedAggregator = 'freekassa'">
                  <img src="~/assets/images/aggregators/freekassa.png" alt="freekassa" width="100" height="32">
                </div>
                <div v-if="selected.price != 0" class="aggregator_btn" id="enot" @click="selectedAggregator = 'enot'">
                  <img src="~/assets/images/aggregators/enot.png" alt="enot" width="100" height="32">
                </div>
                <div v-if="selected.price != 0" class="aggregator_btn" id="crystalpay" @click="selectedAggregator = 'crystalpay'">
                  <img src="~/assets/images/aggregators/crystalpay.png" alt="crystalpay" width="100" height="32">
                </div>
              </div>
              <div class="modal-action">
                <input type="submit" id="feimisio_btn" class="feimisio_btn" @click="confirmModal" value="Приобрести">
              </div>
            </div>
          </form>
        </v-tailwind-modal>
      </div>
    </main>
</template>