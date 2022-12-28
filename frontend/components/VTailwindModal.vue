<template>
  <vue-final-modal
    v-slot="{ params, close }"
    v-bind="$attrs"
    classes="flex justify-center items-center"
    content-class="relative modal-box max-h-full"
  >
    <button class="btn btn-ghost btn-square absolute right-2 top-2 mr-2" @click="$emit('cancel', close)">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
    </button>
    <slot name="title"></slot>
    <slot :params="params"></slot>
  </vue-final-modal>
</template>

<script>
import { $vfm, VueFinalModal, ModalsContainer } from 'vue-final-modal'

export default {
  name: 'VTailwindModal',
  inheritAttrs: false,
  emits: ['cancel'],
  components: {
    VueFinalModal,
    ModalsContainer
  }
}
</script>
