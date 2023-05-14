import config from '~/config/config.js';

async function getPrivilegeByUID(uid) {
  return await $fetch(`${config.siteAPIDomain}/api/privilege?uid=${uid}`);
}

export { getPrivilegeByUID };