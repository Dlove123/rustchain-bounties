//! Wallet commands implementation

use crate::wallet::Wallet;

pub fn create_wallet(name: Option<String>) {
    let wallet_name = name.unwrap_or_else(|| "default".to_string());
    let wallet = Wallet::new();
    println!("✅ Created wallet '{}'", wallet_name);
    println!("Address: {}", wallet.address);
}

pub fn check_balance(address: Option<String>) {
    let addr = address.unwrap_or_else(|| "default".to_string());
    println!("Balance for {}: 0 RTC", addr);
}

pub fn send_rtc(to: String, amount: u64) {
    println!("Sending {} RTC to {}", amount, to);
}

pub fn show_history(limit: Option<usize>) {
    println!("Transaction history (limit: {:?})", limit);
}

pub fn export_wallet(confirm: bool) {
    if !confirm {
        println!("⚠️ Use --confirm to export private key");
        return;
    }
    println!("Private key: [REDACTED]");
}

pub fn import_wallet(key: String) {
    println!("Importing wallet with key: {}...", &key[..8]);
}
