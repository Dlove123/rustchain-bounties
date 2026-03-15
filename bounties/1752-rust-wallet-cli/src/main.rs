//! RustChain Wallet CLI - Native Rust wallet for RustChain blockchain
//! 
//! Features:
//! - Create new wallets
//! - Check balance via RPC
//! - Send RTC transactions
//! - View transaction history
//! - Export/Import private keys

use clap::{Parser, Subcommand};
use serde::{Deserialize, Serialize};
use std::path::PathBuf;

mod wallet;
mod rpc;
mod commands;
mod error;

#[derive(Parser)]
#[command(name = "rustchain-wallet")]
#[command(author = "Dlove123")]
#[command(version = "0.1.0")]
#[command(about = "Native Rust wallet CLI for RustChain blockchain", long_about = None)]
struct Cli {
    /// RPC endpoint URL
    #[arg(long, default_value = "https://50.28.86.131")]
    rpc_url: String,

    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Create a new wallet
    Create {
        /// Wallet name
        #[arg(short, long)]
        name: Option<String>,
    },
    
    /// Show wallet balance
    Balance {
        /// Wallet address
        #[arg(short, long)]
        address: Option<String>,
    },
    
    /// Send RTC to another address
    Send {
        /// Recipient address
        #[arg(short, long)]
        to: String,
        /// Amount in RTC
        #[arg(short, long)]
        amount: u64,
    },
    
    /// List all transactions
    History {
        /// Limit number of transactions
        #[arg(short, long)]
        limit: Option<usize>,
    },
    
    /// Export wallet private key
    Export {
        /// Confirm export
        #[arg(long)]
        confirm: bool,
    },
    
    /// Import wallet from private key
    Import {
        /// Private key (hex)
        #[arg(short, long)]
        key: String,
    },
    
    /// Show wallet address
    Address,
}

fn main() {
    if let Err(e) = run() {
        eprintln!("Error: {}", e);
        std::process::exit(1);
    }
}

fn run() -> Result<(), Box<dyn std::error::Error>> {
    let cli = Cli::parse();
    
    match cli.command {
        Commands::Create { name } => {
            commands::create_wallet(name)?;
        }
        Commands::Balance { address } => {
            commands::check_balance(address, &cli.rpc_url)?;
        }
        Commands::Send { to, amount } => {
            commands::send_rtc(to, amount, &cli.rpc_url)?;
        }
        Commands::History { limit } => {
            commands::show_history(limit, &cli.rpc_url)?;
        }
        Commands::Export { confirm } => {
            commands::export_wallet(confirm)?;
        }
        Commands::Import { key } => {
            commands::import_wallet(key)?;
        }
        Commands::Address => {
            commands::show_address()?;
        }
    }
    
    Ok(())
}
