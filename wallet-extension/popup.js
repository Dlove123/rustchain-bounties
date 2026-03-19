/**
 * RustChain Wallet - Popup UI Controller
 */
let currentWallet = null;
let generatedSeedPhrase = null;

document.addEventListener('DOMContentLoaded', async () => { await checkWalletStatus(); });

async function checkWalletStatus() {
  try {
    currentWallet = await WalletCore.loadWallet();
    if (currentWallet) { showMainWallet(); } else { showWelcome(); }
  } catch (error) { showWelcome(); }
}

function showWelcome() {
  hideAllScreens();
  document.getElementById('welcome-screen').classList.remove('hidden');
}

function showCreateWallet() {
  hideAllScreens();
  document.getElementById('create-screen').classList.remove('hidden');
}

function showImportWallet() {
  hideAllScreens();
  document.getElementById('import-screen').classList.remove('hidden');
}

function showMainWallet() {
  hideAllScreens();
  document.getElementById('wallet-screen').classList.remove('hidden');
  document.getElementById('wallet-address').textContent = currentWallet.address;
  refreshBalance();
}

function hideAllScreens() {
  document.getElementById('welcome-screen').classList.add('hidden');
  document.getElementById('create-screen').classList.add('hidden');
  document.getElementById('import-screen').classList.add('hidden');
  document.getElementById('wallet-screen').classList.add('hidden');
}

async function generateWallet() {
  try {
    generatedSeedPhrase = await WalletCore.generateSeedPhrase();
    const words = generatedSeedPhrase.split(' ');
    document.getElementById('seed-phrase-display').innerHTML = words.map((w, i) => 
      `<div style="background: rgba(255,255,255,0.2); padding: 8px; border-radius: 4px; text-align: center; font-size: 12px;">${i + 1}. ${w}</div>`
    ).join('');
    document.getElementById('seed-phrase-display').classList.remove('hidden');
    document.getElementById('confirm-section').classList.remove('hidden');
    document.getElementById('generate-btn').disabled = true;
  } catch (error) { alert('Error generating wallet'); }
}

function toggleCreateButton() {
  document.getElementById('create-btn').disabled = !document.getElementById('confirm-backup').checked;
}

async function createWallet() {
  try {
    const keypair = await WalletCore.deriveKeypair(generatedSeedPhrase);
    const address = WalletCore.generateAddress(keypair.publicKey);
    await WalletCore.saveWallet(generatedSeedPhrase, keypair, address);
    currentWallet = { seedPhrase: generatedSeedPhrase, ...keypair, address };
    setTimeout(() => { showMainWallet(); }, 1000);
  } catch (error) { alert('Error creating wallet'); }
}

async function importWallet() {
  try {
    const seedPhrase = document.getElementById('import-seed').value.trim().toLowerCase();
    if (!seedPhrase || seedPhrase.split(/\s+/).length < 12) {
      alert('Please enter at least 12 words'); return;
    }
    const keypair = await WalletCore.deriveKeypair(seedPhrase);
    const address = WalletCore.generateAddress(keypair.publicKey);
    await WalletCore.saveWallet(seedPhrase, keypair, address);
    currentWallet = { seedPhrase, ...keypair, address };
    setTimeout(() => { showMainWallet(); }, 1000);
  } catch (error) { alert('Error importing wallet'); }
}

async function refreshBalance() {
  try {
    const balance = await WalletCore.checkBalance(currentWallet.address);
    document.getElementById('balance').textContent = balance.balance;
    document.getElementById('balance-usd').textContent = balance.usdValue;
  } catch (error) {}
}

function copyAddress() {
  navigator.clipboard.writeText(currentWallet.address).then(() => alert('Address copied!'));
}

function logout() {
  currentWallet = null;
  WalletCore.clearWallet();
  showWelcome();
}
