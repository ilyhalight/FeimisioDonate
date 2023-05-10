<script setup>
    const props = defineProps({
    title: {
      type: String,
      required: true
    },
    content: {
      type: String,
      required: true
    }
  });
</script>


<template>
    <details>
      <summary>
        <span class="summary-title">{{ title }}</span>
        <div class="summary-icon-hidden">
          <Icon name="fluent:chevron-down-24-filled"/>
        </div>
      </summary>
      <div class="summary-content">
        <slot name="content"></slot>
      </div>
      <div class="summary-icon-opened">
        <Icon name="fluent:chevron-up-24-filled"/>
      </div>
  </details>
</template>