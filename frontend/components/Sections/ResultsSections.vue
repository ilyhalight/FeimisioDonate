<script setup>
    const props = defineProps({
    imgBackground: {
      type: String,
      required: false
    },
    resultTitle: {
      type: String,
      required: true
    },
    resultDescription: {
      type: String,
      required: true
    }
  });
</script>

<template>
  <section class="result-section">
    <div class="result">
      <div class="result-top animate-pulse" :style="imgBackground ? 'background:'+imgBackground+';' : ''">
        <slot name="result-image"></slot>
      </div>
      <div class="results-content">
        <div class="results-texts">
          <h3 class="title">{{ resultTitle }}</h3>
          <p class="description">{{ resultDescription }}</p>
        </div>
        <div class="results-buttons">
          <NuxtLink to="/support" class="button gradient">{{ $t("The privilege didn't come") }}?</NuxtLink>
          <NuxtLink to="/" class="button gradient">← {{ $t('To the main page') }}</NuxtLink>
        </div>
      </div>
    </div>

  </section>
</template>