<script setup>
  useHead({
    title: "Поддержка · Feimisio Donate",
    meta: [
      {
        name: "og:title",
        content: "Поддержка - Feimisio Donate"
      },
    ]
  });
</script>

<template>
    <main class="centered_container m-6 mt-2 md:mt-12 flex flex-col items-center">
      <section class="mt-16 md:mt-0 shadow-lg w-2/3 p-4 lg:w-1/3 flex flex-col items-center rounded-lg">
        <div class="md:-mt-16 bg-info/20 animate-pulse rounded-full">
          <svg class="text-info  w-36 animate-none" data-darkreader-inline-stroke="" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9 5.25h.008v.008H12v-.008z" stroke-linecap="round" stroke-linejoin="round"></path>
          </svg>
        </div>
        <div class="py-10 text-center">
          <p class="text-3xl font-bold">Техническая поддержка</p>
          <p class="text-xl">Для перехода к группе с технической поддержкой нажмите на одну из иконок представленных ниже</p>
        </div>
        <div class="flex max-sm:flex-col items-center">
          <a href="https://vk.me/feimisio" class="btn_ghost max-sm:m-2" target="_blank">
            <img class="p-1" alt="VK" src="~/assets/images/social/vk.svg" width="48" height="48"/>
          </a>
          <a href="https://discord.gg/mvWQEePJAn" class="btn_ghost max-sm:m-2" target="_blank">
            <img alt="Discord" src="~/assets/images/social/discord.svg" width="48" height="48"/>
          </a>
          <a href="https://t.me/feimisio" class="btn_ghost max-sm:m-2" target="_blank">
            <img class="p-1" alt="Telegram" src="~/assets/images/social/telegram.svg" width="48" height="48"/>
          </a>
          <a href="https://github.com/ilyhalight/FeimisioDonate/" class="btn_ghost max-sm:m-2" target="_blank">
            <img class="p-1" alt="Github" src="~/assets/images/social/github.svg" width="48" height="48"/>
          </a>
        </div>
        <div class="w-2/3 mt-10">
          <NuxtLink to="/" class="feimisio_full_btn">← На главную</NuxtLink>
        </div>
      </section>
    </main>
</template>