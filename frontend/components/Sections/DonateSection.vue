<script setup>
  import { ModalsContainer, useModal, useModalSlot } from 'vue-final-modal';
  import ModalFull from '~/components/Modals/ModalFull.vue'
  import { normalizePrice, normalizeDuration, getFinalPrice } from '~/utils/normalize.js';
  import { getPrivileges } from '~/utils/getPrivileges.js';
  import DonateForm from '~/components/Forms/DonateForm.vue';
  import config from '~/config/config.js';

  const { t } = useI18n();

  // TODO: Make its loading on client (edits by server)
  const donateList = await useAsyncData(async () => {
    return await getPrivileges();
  });

  const selected = ref({
    uid: 1,
    name: 'VIP',
    price: 10000,
  });

  const privilegeName = computed(() => `${t('Buying')} ${selected.value.name}`);

  const { open, close } = useModal({
    component: ModalFull,
    attrs: {
      title: privilegeName,
      onClose() {
        close();
      },
    },
    slots: {
      default: useModalSlot({
        component: DonateForm,
        attrs: {
          selected: selected,
        }
      })
    },
  });
</script>

<template>
  <section v-if="donateList.data.value.length" class="donates">
    <figure class="card" v-for="donate in donateList.data.value" :key="donate.uid" @click="selected.uid = donate.uid; selected.name = donate.name; selected.price = donate.price; promoCode = ''; open();">
      <div class="card-image">
        <img
          :src="donate.image && donate.image.length ? donate.image : '/images/crown.svg'"
          :alt="donate.name"
          :style="((donate.image && donate.image.length) ? '' : 'padding:56px;')+(donate.bg_color ? `background:${donate.bg_color}` : '')"
        >
        <div class="tags">
          <div class="tag" v-html="normalizeDuration(donate.duration, t)"></div>
        </div>
      </div>
      <figcaption>
        <div class="card-title title">
          <h3>{{ donate.name }}</h3>
          <h3 v-html="getFinalPrice(donate.price, donate.discount, t)"></h3>
        </div>
        <p>{{ $t(donate.short_description) }}</p>
        <NuxtLink :bind="donate.link" :to="'/info/'+donate.link" target="_blank">{{ $t('Detailed') }}...</NuxtLink>
      </figcaption>
    </figure>
    <ModalsContainer />
  </section>
</template>