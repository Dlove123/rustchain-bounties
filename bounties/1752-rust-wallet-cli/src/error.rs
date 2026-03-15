//! Error types for rustchain-wallet

use thiserror::Error;

#[derive(Error, Debug)]
pub enum WalletError {
    #[error("Wallet not found: {0}")]
    NotFound(String),
    
    #[error("Invalid private key: {0}")]
    InvalidKey(String),
    
    #[error("RPC error: {0}")]
    RpcError(String),
    
    #[error("IO error: {0}")]
    IoError(#[from] std::io::Error),
    
    #[error("JSON error: {0}")]
    JsonError(#[from] serde_json::Error),
}
