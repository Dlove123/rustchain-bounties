document.getElementById('checkBtn').addEventListener('click', async () => {
  const address = document.getElementById('address').value.trim();
  const resultDiv = document.getElementById('result');
  
  if (!address) {
    resultDiv.innerHTML = '<p class="error">Please enter an address</p>';
    return;
  }
  
  try {
    const response = await fetch('https://rpc.rustchain.com', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        method: 'eth_getBalance',
        params: [address, 'latest'],
        id: 1
      })
    });
    const data = await response.json();
    if (data.result) {
      const balance = parseInt(data.result, 16) / 1e18;
      resultDiv.innerHTML = `<p>${balance.toFixed(4)} RTC</p>`;
    } else {
      resultDiv.innerHTML = '<p class="error">Error fetching balance</p>';
    }
  } catch (error) {
    resultDiv.innerHTML = '<p class="error">Network error</p>';
  }
});
