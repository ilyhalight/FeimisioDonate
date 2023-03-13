<script setup>
  import { useRoute } from 'vue-router';
  import config from '~/config/config.js';

  const route = useRoute();
  const id = route.params.id;
  const { t } = useI18n();

  const privilegeInfo = ref([]);

  privilegeInfo.value = await getPrivilegeInfoByName(id);
  if (!privilegeInfo.value) {
    throw createError({ statusCode: 404, message: t('Unknown privilege'), fatal: true})
  }

  useServerSeoMeta ({
    title: id,
    // ogTitle: id,
    description: `${t('Information about')} ${id}`,
    // ogDescription: `${t('Information about')} ${id}`
  });
</script>


<template>
  <main class="wrapper">
    <Breadcrumbs>
      <template #breadcrumb="{ to, title }">
        <NuxtLink :to="to">
          <template v-if="!title.toLowerCase().includes(id.toLowerCase())">
            {{ $t(title) }}
          </template>
          <template v-else>
            {{ id }}
          </template>
        </NuxtLink>
      </template>
    </Breadcrumbs>
    <template v-if="privilegeInfo.length">
      <p class="text-attractive center">
        {{ $t('Information about')}}
        <span class="text-gradient">
          {{ privilegeInfo[0].link }}
        </span>
      </p>
      <section class="privilege_info">
        <div v-for="privilege in privilegeInfo" :key="privilege.uid" class="block" :class="(privilege.img_link ? 'has-img': '') + (privilege.is_big_img ? ' big': '') + (privilege.img_reverse_side ? ' reverse' : '')">
          <img v-if="privilege.img_link" :class="privilege.is_big_img ? 'big' : ''" :src="privilege.img_link" :alt="$t(privilege.name)+' '+$t('example')">
          <div class="text-block" :class="privilege.is_big_img ? 'big' : 'small'">
            <p class="title">{{ $t(privilege.name) }}</p>
            <p class="subtext" :class="privilege.img_reverse_side ? 'reverse': ''">{{ $t(privilege.desc) }}</p>
          </div>
        </div>
      </section>
    </template>
    <template v-else>
      <p class="text-attractive center">
        {{ $t('Connection error') }}
      </p>
    </template>
  </main>
</template>