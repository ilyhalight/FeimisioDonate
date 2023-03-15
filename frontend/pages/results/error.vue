<script setup>
  import ResultsSections from '~/components/Sections/ResultsSections.vue';
  definePageMeta({
    title: 'The payment failed'
  });
</script>

<template>
  <main class="wrapper">
    <results-sections imgBackground="var(--error-20)" :resultTitle="$t('The payment failed')+'!'" :resultDescription="$t('Do not worry if you have made a payment and the privilege has not come to you - contact Technical support.')">
      <template #result-image>
        <svg class="error" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke-linecap="round" stroke-linejoin="round"></path>
        </svg>
      </template>
    </results-sections>
  </main>
</template>