<template>
  <header class="centered_container">
    <div class="navbar">
      <div class="navbar-start">
        <NuxtLink class="logo" to="/">
          <div class="avatar mx-5">
            <div class="w-10 rounded-md">
              <img alt="logo" src="~/assets/images/logo.svg" />
            </div>
          </div>
          FeimisioDonate
        </NuxtLink>
      </div>
      <div class="navbar-end">
        <ThemeSelector/>
        <a href="https://github.com/ilyhalight/FeimisioDonate/" class="btn_ghost max-sm:m-2" target="_blank">
          <img class="p-1" alt="Github" src="~/assets/images/social/github.svg" width="36" height="36"/>
        </a>
      </div>
    </div>
  </header>
</template>
