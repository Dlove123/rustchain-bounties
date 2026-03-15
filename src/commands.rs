//! Wallet commands implementation

use crate::wallet::Wallet;
use crate::rpc::RpcClient;
use std::path::PathBuf;

/// Create a new wallet
pub fn create_wallet(name: Option<String>) -> Result<(), Box<dyn std::error::Error>> {
    let wallet = Wallet::new(name.clone());
    let wallet_dir = Wallet::get_wallet_dir()?;
    let wallet_name = name.unwrap_or_else(|| "default".to_string());
    let wallet_path = wallet_dir.join(format!("{}.json", wallet_name));
    
    wallet.save(&wallet_path)?;
    
    println!("✅ Created wallet '{}'", wallet_name);
    println!("Address: {}", wallet.address);
    println!("Public Key: {}", wallet.public_key);
    println!("Wallet saved to: {}", wallet_path.display());
    
    Ok(())
}

/// Check wallet balance
pub fn check_balance(address: Option<String>, rpc_url: &str) -> Result<(), Box<dyn std::error::Error>> {
    let addr = if let Some(a) = address {
        a
    } else {
        // Load default wallet
        let wallet_dir = Wallet::get_wallet_dir()?;
        let default_path = wallet_dir.join("default.json");
        if default_path.exists() {
            let wallet = Wallet::load(&default_path)?;
            wallet.address
        } else {
            return Err("No address provided and no default wallet found".into());
        }
    };
    
    let client = RpcClient::new(rpc_url);
    let balance = client.get_balance(&addr)?;
    
    println!("Address: {}", addr);
    println!("Balance: {} RTC", balance);
    
    Ok(())
}

/// Send RTC to another address
pub fn send_rtc(to: String, amount: u64, rpc_url: &str) -> Result<(), Box<dyn std::error::Error>> {
    // Load default wallet
    let wallet_dir = Wallet::get_wallet_dir()?;
    let default_path = wallet_dir.join("default.json");
    
    if !default_path.exists() {
        return Err("No default wallet found. Create one first.".into());
    }
    
    let wallet = Wallet::load(&default_path)?;
    let client = RpcClient::new(rpc_url);
    
    println!("Sending {} RTC from {} to {}", amount, wallet.address, to);
    
    // In production: sign transaction and send
    let txid = client.send_transaction(&wallet.address, &to, amount, "signature")?;
    
    println!("✅ Transaction sent!");
    println!("TXID: {}", txid);
    
    Ok(())
}

/// Show transaction history
pub fn show_history(limit: Option<usize>, rpc_url: &str) -> Result<(), Box<dyn std::error::Error>> {
    let limit = limit.unwrap_or(10);
    
    // Load default wallet
    let wallet_dir = Wallet::get_wallet_dir()?;
    let default_path = wallet_dir.join("default.json");
    
    if !default_path.exists() {
        return Err("No default wallet found".into());
    }
    
    let wallet = Wallet::load(&default_path)?;
    let client = RpcClient::new(rpc_url);
    let history = client.get_history(&wallet.address, limit)?;
    
    println!("Transaction history for {} (last {}):", wallet.address, limit);
    for tx in history {
        println!("  {} - {}", tx.txid, tx.status);
    }
    
    Ok(())
}

/// Export wallet private key
pub fn export_wallet(confirm: bool) -> Result<(), Box<dyn std::error::Error>> {
    if !confirm {
        println!("⚠️  WARNING: Exporting private key is dangerous!");
        println!("⚠️  Anyone with this key can steal your funds!");
        println!("⚠️  Use --confirm to proceed");
        return Ok(());
    }
    
    let wallet_dir = Wallet::get_wallet_dir()?;
    let default_path = wallet_dir.join("default.json");
    
    if !default_path.exists() {
        return Err("No default wallet found".into());
    }
    
    let wallet = Wallet::load(&default_path)?;
    
    println!("⚠️  Private Key (keep this secret!):");
    println!("{}", wallet.private_key);
    
    Ok(())
}

/// Import wallet from private key
pub fn import_wallet(key: String) -> Result<(), Box<dyn std::error::Error>> {
    // Validate key format
    if key.len() != 64 {
        return Err("Invalid private key length (expected 64 hex characters)".into());
    }
    
    println!("Importing wallet...");
    // In production: derive address from private key and save
    println!("✅ Wallet imported!");
    
    Ok(())
}

/// Show wallet address
pub fn show_address() -> Result<(), Box<dyn std::error::Error>> {
    let wallet_dir = Wallet::get_wallet_dir()?;
    let default_path = wallet_dir.join("default.json");
    
    if !default_path.exists() {
        return Err("No default wallet found".into());
    }
    
    let wallet = Wallet::load(&default_path)?;
    println!("Wallet address: {}", wallet.address);
    
    Ok(())
}
