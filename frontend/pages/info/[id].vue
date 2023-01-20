<script setup>
  import { useRoute } from 'vue-router'
  const route = useRoute()
  const id = route.params.id;
  useHead({
    title: `${id} · Feimisio Donate`,
    meta: [
      {
        name: "og:title",
        content: `${id} - Feimisio Donate`
      },
    ]
  });
</script>


<template>
  <main class="centered_container m-6 mt-2 md:mt-6">
    <template v-if="privillegeInfo.length">
      <div class="flex flex-col items-center">
        <p class="text-2xl">Информация о {{ privillegeInfo[0].link }}</p>
        <NuxtLink to="/" class="donate_link">← Вернуться назад</NuxtLink>
      </div>
      <section class="flex flex-col md:flex-row flex-wrap mt-4 justify-center">
          <div v-for="privillege in privillegeInfo" :key="privillege.uid" 
          class="flex m-4 p-4"
          :class="
            (privillege.img_link && privillege.is_big_img ?
              privillege.img_reverse_side ?
                'flex-col-reverse md:flex-row-reverse' : 'flex-col md:flex-row'
              : privillege.img_link ?
                  privillege.img_reverse_side ?
                    'flex-row-reverse' : 'flex-row'
                : 'flex-col')+
            (privillege.is_big_img ? ' w-66 md:w-[100%]' : ' w-76 md:w-96')">
              <img v-if="privillege.img_link" class="rounded-lg" :class="privillege.is_big_img ? 'max-w-sm w-[95%] md:max-w-md md:w-full h-full' : 'w-36 h-36'" :src="privillege.img_link" :alt="privillege.name+' пример'">
              <template v-if="privillege.img_link">
                <div class="flex-col mt-4 md:mt-0" :class="privillege.is_big_img ? 'w-full md:m-4' : 'm-4'">
                  <p class="text-start font-bold text-xl">{{ privillege.name }}</p>
                  <p class="text-start text-md" :class="privillege.img_reverse_side ? 'mb-4 md:mb-0': ''">{{ privillege.desc }}</p>
                </div>
              </template>
              <template v-else>
                <p class="text-start font-bold text-xl">{{ privillege.name }}</p>
                <p class="text-start text-md">{{ privillege.desc }}</p>
              </template>
          </div>
      </section>
    </template>
    <template v-else>
      <div class="flex flex-col items-center animate-pulse">
        <div class="loading_default w-64"></div>
        <div class="loading_default w-48"></div>
      </div>
      <section class="flex flex-col md:flex-row flex-wrap mt-4 justify-between animate-pulse">
        <div v-for="i in [1,2,3]" :key="i" class="flex m-4 p-4 flex-row w-76 md:w-96">
          <div class="w-36 bg-neutral rounded"></div>
          <div class="flex-col mt-4 md:mt-0 m-4">
            <div class="loading_default w-28"></div>
            <div class="loading_default w-40"></div>
            <div class="loading_default w-44"></div>
            <div class="loading_default w-36"></div>
          </div>
        </div>
        <div class="flex m-4 p-4 flex-col md:flex-row w-66 md:w-[100%]">
          <div class="max-w-sm w-[95%] md:max-w-md md:w-full h-80 bg-neutral rounded"></div>
          <div class="flex-col mt-4 md:mt-0 w-full md:m-4">
            <div class="loading_default w-64"></div>
            <div class="loading_default w-full"></div>
            <div class="loading_default w-[99%]"></div>
            <div class="loading_default w-96"></div>
          </div>
        </div>
        <div class="flex m-4 p-4 flex-col md:flex-row-reverse w-66 md:w-[100%]">
          <div class="max-w-sm w-[95%] md:max-w-md md:w-full h-80 bg-neutral rounded"></div>
          <div class="flex-col mt-4 md:mt-0 w-full md:m-4">
            <div class="loading_default w-64"></div>
            <div class="loading_default w-full"></div>
            <div class="loading_default w-[99%]"></div>
            <div class="loading_default w-96"></div>
          </div>
        </div>
      </section>
    </template>
  </main>
</template>

<script>
  export default {
    data() {
      return {
        privillegeInfo: []
      }
    },

    created: async function() {
      const { id } = this.$route.params;
      const privillegeData = await $fetch(
        `http://127.0.0.1:3312/api/privillege/info?name=${id}`
      );
      if (privillegeData) {
        this.privillegeInfo = privillegeData;
      } else {
        throw createError({ statusCode: 404, message: 'Вы пытаетесь найти информацию о неизвестной привилегии.', fatal: true})
        // fatal:
        // false - only server error
        // true - client & server error (show block with error)
      }
    }
  }
</script>