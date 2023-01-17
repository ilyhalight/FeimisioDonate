<script setup>
  useHead({
    title: "Платеж не удался · Feimisio Donate",
    meta: [
      {
        name: "og:title",
        content: "Платеж не удался - Feimisio Donate"
      },
    ]
  });
</script>

<template>
    <main class="centered_container m-6 mt-2 md:mt-12 flex flex-col items-center">
      <section class="mt-16 md:mt-0 shadow-lg w-2/3 p-4 lg:w-1/3 flex flex-col items-center rounded-lg">
        <div class="md:-mt-16 bg-error/20 animate-pulse rounded-full">
          <svg class="text-error w-36 animate-none" data-darkreader-inline-stroke="" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke-linecap="round" stroke-linejoin="round"></path>
          </svg>
        </div>
        <div class="py-10 text-center">
          <p class="text-3xl font-bold">Платеж не удался!</p>
          <p class="text-xl">Не беспокойтесь, если вы совершили оплату и привилегия вам не пришла - обратитесь в Тех. поддержку.</p>
        </div>
        <div>
          <NuxtLink to="/support" class="feimisio_full_btn my-4">Тех. поддержка</NuxtLink>
          <NuxtLink to="/" class="feimisio_full_btn my-4">← На главную</NuxtLink>
        </div>
      </section>
    </main>
</template>