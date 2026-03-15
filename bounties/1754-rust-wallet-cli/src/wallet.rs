//! Wallet management module

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Wallet {
    pub address: String,
    pub private_key: String,
    pub created_at: u64,
}

impl Wallet {
    pub fn new() -> Self {
        // Generate new wallet
        Self {
            address: String::new(),
            private_key: String::new(),
            created_at: std::time::UNIX_EPOCH.elapsed().unwrap().as_secs(),
        }
    }
    
    pub fn save(&self, path: &str) -> std::io::Result<()> {
        let json = serde_json::to_string_pretty(self)?;
        std::fs::write(path, json)
    }
}
