<script setup>
  import config from '~/config/config.js'
</script>

<template>
  <footer class="footer">
    <div class="footer-logo">
      <NuxtLink to="/" >
        <nuxt-img src="/images/logo.svg" :alt="config.siteName"/>
      </NuxtLink>
      <p>
        {{ $t('We have nothing to do with Valve Corporation')}}.
        <br>
        <strong>{{ config.siteName }} © 2023</strong>
      </p>
    </div>

    <div class="footer-links">
      <a :href="config.siteRedirectDomain">{{ $t('Main') }}</a>
      <a :href="config.siteUserAgreement">{{ $t('User agreement') }}</a>
      <a href="/api/redoc">API</a>
    </div>
  </footer>
</template>