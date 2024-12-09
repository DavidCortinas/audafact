// Create a browser-agnostic storage utility
const storage = {
  get: async (keys) => {
    if (typeof browser !== 'undefined' && browser.storage) {
      return browser.storage.local.get(keys);
    }
    return new Promise((resolve) => {
      chrome.storage.local.get(keys, resolve);
    });
  },

  set: async (items) => {
    if (typeof browser !== 'undefined' && browser.storage) {
      return browser.storage.local.set(items);
    }
    return new Promise((resolve) => {
      chrome.storage.local.set(items, resolve);
    });
  },

  remove: async (keys) => {
    if (typeof browser !== 'undefined' && browser.storage) {
      return browser.storage.local.remove(keys);
    }
    return new Promise((resolve) => {
      chrome.storage.local.remove(keys, resolve);
    });
  },

  clear: async () => {
    if (typeof browser !== 'undefined' && browser.storage) {
      return browser.storage.local.clear();
    }
    return new Promise((resolve) => {
      chrome.storage.local.clear(resolve);
    });
  }
};

export default storage;
