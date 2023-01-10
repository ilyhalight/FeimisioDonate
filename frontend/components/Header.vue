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
      </div>
    </div>
  </header>
</template>
