<script setup>
  import BlockLoading from "~/components/donate/BlockLoading.vue";
  import VTailwindModal from "~/components/VTailwindModal.vue";
  useHead({
    title: "Главная · Fame Donate",
    meta: [
      {
        name: "og:title",
        content: "Главная - Fame Donate"
      },
    ]
  });
</script>

<template>
  <main class="centered_container m-6 mt-2 md:mt-6">
    <p class="page_title">Донат</p>
    <section class="donate_section">
        <template v-if="donateList.length">
          <div v-for="donate in donateList" :key="donate.uid" class="donate_block">
            <p class="donate_title">{{ donate.name }}</p>
            <p class="donate_price" v-html="getFinalPrice(donate.duration, donate.price, donate.discount)"></p>
            <!-- TODO: Доделать показ срока и скидки -->
            <div class="text-xl mt-4 mb-4">Вы получите доступ к:
                <ul class="donate_features">
                  <li v-for="feature in donate.short_description.split(';')" :key="feature">{{ feature }}</li>
                </ul>   
                <a class="donate_link" :bind="donate.link" :href="'/info/'+donate.link" target="_blank">Подробнее...</a>
            </div>
            <label :key="donate.uid" :id="'buy_'+donate.uid" class="donate_btn" @click="selected.uid = donate.uid; selected.name = donate.name; modalShow = true">Приобрести</label>
          </div>
        </template>
        <template v-else>
          <BlockLoading/>
        </template>
    </section>
    <div>
      <v-tailwind-modal v-model="modalShow" @cancel="cancelModal">
        <form class="-mt-2" method="post" action="https://donate.fame-community.ru/api/payments-methods">
          <p class="text-center text-xl font-bold">Покупка {{ selected.name }}</p>
          <div class="mt-4">
            <label class="block mb-2" for="steam_link">
              Введите ссылку на <a class="donate_link" href="https://steamcommunity.com/">Steam</a> профиль:
            </label>
            <label class="text-error hidden" id="steam_link_error" for="steam_link">
              Ссылка не введена
            </label>
            <input v-model="steamLink" class="text_input" id="steam_link" name="steam_link" type="url" placeholder="https://steamcommunity.com/id/ToilOfficial" autocomplete="on" required>
            <!-- TODO: Добавить платежки -->
            <input type="hidden" :value="selected.uid" name="uid">
            <input type="hidden" :value="selectedAggregator" name="aggregator">
            <p class="block mt-4">Выберите платежную систему:</p>
            <div class="flex flex-wrap justify-between" id="aggregators">
              <div class="aggregator_btn active" id="freekassa" @click="selectedAggregator = 'freekassa'">
                <img src="~/assets/images/aggregators/freekassa.png" alt="freekassa" width="100" height="32">
              </div>
              <div class="aggregator_btn" id="enot" @click="selectedAggregator = 'enot'">
                <img src="~/assets/images/aggregators/enot.png" alt="enot" width="100" height="32">
              </div>
              <div class="aggregator_btn" id="crystalpay" @click="selectedAggregator = 'crystalpay'">
                <img src="~/assets/images/aggregators/crystalpay.png" alt="crystalpay" width="100" height="32">
              </div>
            </div>
            <!-- <label class="block mb-2 mt-4" for="promocode">
              Введите промокод (если есть)
            </label>
            <label class="text-error hidden" id="promocode_error" for="promocode">
              Промокод не найден
            </label>
            <input v-model="promoCode" class="text_input" id="promocode" name="Ссылка на Steam профиль" type="text" placeholder="Промокод" autocomplete="off"> -->
            <div class="modal-action">
              <input type="submit" class="donate_btn" @click="confirmModal" value="Приобрести">
            </div>
          </div>
        </form>
      </v-tailwind-modal>
    </div>
  </main>
</template>

<script>
export default {
  data() {
    return {
      donateList: [],
      selectedAggregator: 'freekassa',
      steamLink: '',
      promoCode: '',
      modalShow: false,
      selected: {
        uid: 1,
        name: 'VIP',
      }
    }
  },

  created: async function() {
    const data = await $fetch(
      "https://donate.fame-community.ru/api/privilleges"
    );
    if (data) {
      this.donateList = data;
    }
  },

  methods: {
    normalizePrice(price, discount) {
      if (price === 0) {
        return "Бесплатно";
      } else {
        if (discount === 0) {
          return `${price}₽`;
        } else {
          return `${Math.round(price - (price / 100 * discount))}₽`
        }
      }
    },
    normalizeDuration(duration) {
      if (duration === 0) {
        return 'навсегда';
      } else if (duration % 24 === 0 && duration / 24 % 30 === 0) {
        return `${duration / 24 / 30 === 1 ? '' : `${duration / 24 / 30} `}мес.`;
      } else if (duration % 24 === 0) {
        return `${duration / 24} дн`;
      } else {
        return `${duration} час.`;
      }
    },
    getFinalPrice(duration, price, discount) {
      let priceNormalized = this.normalizePrice(price, discount);
      let durationNormalized = this.normalizeDuration(duration);
      let durationBlock = `<small class="donate_expire">/${durationNormalized}</small>`
      if (discount > 0 && price > 0) {
        return `<span class="line-through">${price}₽${durationBlock}</span><br> <span class="text-red-400">${priceNormalized}${durationBlock}</span>`;
      } else {
        return `${priceNormalized}${durationBlock}`;
      }
    },
    confirmModal() {
      let steamLink = document.getElementById('steam_link').value;
      let steamLinkError = document.getElementById('steam_link_error');
      if (steamLink && /^(https:\/\/|http:\/\/)?steamcommunity.com\/(id|profiles)\/.*$/.test(steamLink)) {
        this.modalShow = false;
      } else if (steamLink) {
        steamLinkError.textContent = 'Ссылка не валидна';
        steamLinkError.classList.remove('hidden');
      } else {
        steamLinkError.textContent = 'Ссылка не введена';
        steamLinkError.classList.remove('hidden');
      }
    },
    cancelModal(close) {
      this.modalShow = false;
    }
  },

  watch: {
    selectedAggregator() {
      let aggregatorBtns = document.getElementById('aggregators').children;
      for (let i = 0; i < aggregatorBtns.length; i++) {
        aggregatorBtns[i].classList.remove('active');
      }
      document.getElementById(this.selectedAggregator).classList.add('active');
    },
    steamLink() {
      let steamLinkError = document.getElementById('steam_link_error');
      if (this.steamLink && /^(https:\/\/|http:\/\/)?steamcommunity.com\/(id|profiles)\/.*$/.test(this.steamLink)) {
        steamLinkError.classList.add('hidden');
      } else if (this.steamLink) {
        steamLinkError.textContent = 'Ссылка не валидна';
        steamLinkError.classList.remove('hidden');
      } else {
        steamLinkError.textContent = 'Ссылка не введена';
        steamLinkError.classList.remove('hidden');
      }
    },
    // promoCode() {
    //   let promoCodeError = document.getElementById('promocode_error');
    //   if (this.promoCode) {
    //     promoCodeError.classList.remove('hidden');
    //   } else {
    //     promoCodeError.classList.add('hidden');
    //   }
    // }
  }
}
</script>