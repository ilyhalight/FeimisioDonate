<template>
  <ClientOnly>
    <footer class="footer_container">
      <div class="footer_content">
        <div class="footer_logo">
          <NuxtLink to="/">
            <div class="avatar mx-5">
              <div class="w-8 rounded-md">
                <img alt="logo" src="~/assets/images/logo.svg" />
              </div>
            </div>
          </NuxtLink>
          <p>Мы не имеем никакого <br>отношения к Valve Corporation<br/><strong>FeimisioDonate © 2022</strong></p>
        </div>
        <div class="footer_links">
          <a href="https://fame-community.ru" class="footer_link">
            Главная
          </a>
          <a href="https://fame-community.ru/custom/?id=user_agreement" class="footer_link">
            Пользовательское соглашение
          </a>
          <NuxtLink to="/support" class="footer_link">
            Поддержка
          </NuxtLink>
          <a href="/api/redoc" class="footer_link">
            API
          </a>
        </div>
      </div>
    </footer>
  </ClientOnly>
</template>