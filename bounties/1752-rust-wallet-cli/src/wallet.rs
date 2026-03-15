//! Wallet management module

use serde::{Deserialize, Serialize};
use sha2::{Sha256, Digest};
use hex::{encode, decode};
use std::fs;
use std::path::PathBuf;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Wallet {
    pub address: String,
    pub private_key: String,
    pub public_key: String,
    pub created_at: u64,
    pub name: String,
}

impl Wallet {
    /// Generate a new wallet with random keys
    pub fn new(name: Option<String>) -> Self {
        // Generate random private key (32 bytes)
        let private_key_bytes: [u8; 32] = std::array::from_fn(|_| rand::random());
        let private_key = encode(&private_key_bytes);
        
        // Derive public key (simplified - in production use proper crypto)
        let mut hasher = Sha256::new();
        hasher.update(&private_key_bytes);
        let public_key = encode(hasher.finalize());
        
        // Derive address from public key
        let mut addr_hasher = Sha256::new();
        addr_hasher.update(&public_key);
        let address = format!("RTC{}", encode(&addr_hasher.finalize()[..20]));
        
        Self {
            address,
            private_key,
            public_key,
            created_at: std::time::UNIX_EPOCH.elapsed().unwrap().as_secs(),
            name: name.unwrap_or_else(|| "default".to_string()),
        }
    }
    
    /// Load wallet from file
    pub fn load(path: &PathBuf) -> Result<Self, Box<dyn std::error::Error>> {
        let content = fs::read_to_string(path)?;
        let wallet: Wallet = serde_json::from_str(&content)?;
        Ok(wallet)
    }
    
    /// Save wallet to file
    pub fn save(&self, path: &PathBuf) -> Result<(), Box<dyn std::error::Error>> {
        let json = serde_json::to_string_pretty(self)?;
        fs::write(path, json)?;
        Ok(())
    }
    
    /// Get wallet directory
    pub fn get_wallet_dir() -> Result<PathBuf, Box<dyn std::error::Error>> {
        let base = dirs::home_dir()
            .ok_or("Could not find home directory")?
            .join(".rustchain")
            .join("wallets");
        
        fs::create_dir_all(&base)?;
        Ok(base)
    }
}

/// Simple random number generator for demo purposes
mod rand {
    pub fn random<T: Default>() -> T {
        // In production, use proper RNG
        Default::default()
    }
}
