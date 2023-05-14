import config from '~/config/config.js';

async function getPrivileges() {
  return await $fetch(`${config.siteAPIDomain}/api/privileges`, { server: false });
};

async function getPrivilegeInfoByName(name) {
  return await $fetch(`${config.siteAPIDomain}/api/privilege/info?name=${name}`, { server: false });
};

async function getPrivilegeByUID(uid) {
  return await $fetch(`${config.siteAPIDomain}/api/privilege?uid=${uid}`, { server: false });
}

export { getPrivileges, getPrivilegeInfoByName, getPrivilegeByUID };