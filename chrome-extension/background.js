// Background service worker for RustChain Balance extension

// Handle installation
chrome.runtime.onInstalled.addListener(() => {
  console.log('RustChain Balance extension installed');
});

// Handle alarms for auto-refresh
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'refreshBalance') {
    console.log('Auto-refreshing balance...');
  }
});
