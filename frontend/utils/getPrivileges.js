import config from '~/config/config.js';

async function getPrivileges() {
  return await $fetch(`${config.siteAPIDomain}/api/privileges`);
};

async function getPrivilegeInfoByName(name) {
  return await $fetch(`${config.siteAPIDomain}/api/privilege/info?name=${name}`);
};

async function getPrivilegeByUID(uid) {
  return await $fetch(`${config.siteAPIDomain}/api/privilege?uid=${uid}`);
}

export { getPrivileges, getPrivilegeInfoByName, getPrivilegeByUID };