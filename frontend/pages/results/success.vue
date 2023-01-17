<script setup>
  useHead({
    title: "Успешная оплата · Feimisio Donate",
    meta: [
      {
        name: "og:title",
        content: "Успешная оплата - Feimisio Donate"
      },
    ]
  });
</script>

<template>
    <main class="centered_container m-6 mt-2 md:mt-12 flex flex-col items-center">
      <section class="mt-16 md:mt-0 shadow-lg w-2/3 p-4 lg:w-1/3 flex flex-col items-center rounded-lg">
        <div class="md:-mt-16 bg-success/20 animate-pulse rounded-full">
          <svg class="text-success w-36 animate-none" data-darkreader-inline-stroke="" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0112 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.746 3.746 0 011.043 3.296A3.745 3.745 0 0121 12z" stroke-linecap="round" stroke-linejoin="round"></path>
          </svg>
        </div>
        <div class="py-10 text-center">
          <p class="text-3xl font-bold">Успешная оплата!</p>
          <p class="text-xl">Спасибо за вашу поддержку! Ваша привилегия появится в ближайшее время :)</p>
        </div>
        <div>
          <NuxtLink to="/support" class="feimisio_full_btn my-4">Привилегия не пришла?</NuxtLink>
          <NuxtLink to="/" class="feimisio_full_btn my-4">← На главную</NuxtLink>
        </div>
      </section>
    </main>
</template>