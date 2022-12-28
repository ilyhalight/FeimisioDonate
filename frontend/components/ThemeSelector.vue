<template>
  <!-- https://daisyui.com/docs/themes/ -->
  <div title="Change Theme" class="dropdown dropdown-bottom dropdown-end">
    <div tabindex="0" class="btn normal-case btn-ghost">
      <svg
        width="20"
        height="20"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        class="inline-block h-5 w-5 stroke-current md:h-5 md:w-5"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"
        ></path>
      </svg>
      <span class="hidden md:inline">Theme</span>
      <svg
        width="12px"
        height="12px"
        class="ml-1 hidden h-3 w-3 fill-current opacity-60 sm:inline-block"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 2048 2048"
      >
        <path
          d="M1799 349l242 241-1017 1017L7 590l242-241 775 775 775-775z"
        ></path>
      </svg>
    </div>
    <div class="dropdown_content_change_theme dropdown-content" v-if="themes">
      <div class="change_theme_grid" tabindex="0" v-for="theme of themes" :key="theme">
        <div
          class="change_theme_item"
          @click="(colorMode.preference = theme)"
        >
          <div :data-theme="theme" class="change_theme_item_content">
            <div class="change_theme_accent_container">
              <div class="change_theme_accents">
                <div class="change_theme_name">{{ theme }}</div>
                <div class="change_theme_colors">
                  <div class="change_theme_primary_color"></div>
                  <div class="change_theme_secondary_color"></div>
                  <div class="change_theme_accent_color"></div>
                  <div class="change_theme_neutral_color"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  export default {
    data() {
      return {
        colorMode: useColorMode(),
        themes: [
          "light",
          "dark",
          "cupcake",
          "bumblebee",
          "emerald",
          "corporate",
          "synthwave",
          "retro",
          "cyberpunk",
          "valentine",
          "halloween",
          "garden",
          "forest",
          "aqua",
          "lofi",
          "pastel",
          "fantasy",
          "wireframe",
          "black",
          "luxury",
          "dracula",
          "cmyk",
          "autumn",
          "business",
          "acid",
          "lemonade",
          "night",
          "coffee",
          "winter",
        ],
      };
    }
  } 
</script>
