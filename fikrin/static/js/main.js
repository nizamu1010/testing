// pwa script 

if (!navigator.onLine) {
  const offlineMessage = document.createElement('div');
  offlineMessage.textContent = 'You are currently offline. Some features may be limited.';
  offlineMessage.style.backgroundColor = 'red';
  offlineMessage.style.color = 'white';
  offlineMessage.style.padding = '10px';
  offlineMessage.style.textAlign = 'center';
  document.body.insertBefore(offlineMessage, document.body.firstChild);

  // You can also disable or modify certain functionality here
  // For example, disable form submissions or certain buttons
  // document.querySelector('form').setAttribute('disabled', true);
  // document.querySelector('#submit-button').setAttribute('disabled', true);
}
