//! RustChain RPC client module

use serde::{Deserialize, Serialize};
use reqwest::blocking::Client;

pub const DEFAULT_RPC_URL: &str = "https://50.28.86.131";

#[derive(Debug, Serialize, Deserialize)]
pub struct RpcResponse<T> {
    pub jsonrpc: String,
    pub id: u64,
    pub result: Option<T>,
    pub error: Option<RpcError>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct RpcError {
    pub code: i64,
    pub message: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct BalanceResponse {
    pub address: String,
    pub balance: u64,
    pub confirmed: u64,
    pub unconfirmed: u64,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct TransactionResponse {
    pub txid: String,
    pub status: String,
}

pub struct RpcClient {
    client: Client,
    url: String,
}

impl RpcClient {
    pub fn new(url: &str) -> Self {
        Self {
            client: Client::new(),
            url: url.to_string(),
        }
    }
    
    /// Get balance for an address
    pub fn get_balance(&self, address: &str) -> Result<u64, Box<dyn std::error::Error>> {
        // Try the wallet API endpoint
        let url = format!("{}/wallet/balance?miner_id={}", self.url, address);
        let response = self.client.get(&url).send()?;
        
        if response.status().is_success() {
            // Parse response based on actual API format
            Ok(0) // Placeholder - implement based on actual API
        } else {
            Err(format!("RPC request failed: {}", response.status()).into())
        }
    }
    
    /// Send a transaction
    pub fn send_transaction(&self, from: &str, to: &str, amount: u64, signature: &str) 
        -> Result<String, Box<dyn std::error::Error>> 
    {
        let url = format!("{}/wallet/send", self.url);
        let payload = serde_json::json!({
            "from": from,
            "to": to,
            "amount": amount,
            "signature": signature
        });
        
        let response = self.client.post(&url)
            .json(&payload)
            .send()?;
        
        if response.status().is_success() {
            Ok("transaction_sent".to_string())
        } else {
            Err(format!("Transaction failed: {}", response.status()).into())
        }
    }
    
    /// Get transaction history
    pub fn get_history(&self, address: &str, limit: usize) 
        -> Result<Vec<TransactionResponse>, Box<dyn std::error::Error>> 
    {
        let url = format!("{}/wallet/history?address={}&limit={}", self.url, address, limit);
        let response = self.client.get(&url).send()?;
        
        if response.status().is_success() {
            Ok(vec![]) // Placeholder
        } else {
            Err(format!("History request failed: {}", response.status()).into())
        }
    }
}
