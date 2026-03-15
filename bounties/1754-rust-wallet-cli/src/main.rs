//! RustChain Wallet CLI - Native Rust wallet for RustChain blockchain

use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "rustchain-wallet")]
#[command(version = "0.1.0")]
#[command(about = "Native Rust wallet CLI for RustChain")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Create a new wallet
    Create,
    /// Check balance
    Balance { address: Option<String> },
    /// Send RTC
    Send { to: String, amount: u64 },
    /// Show transaction history
    History,
}

fn main() {
    let cli = Cli::parse();
    match cli.command {
        Commands::Create => println!("Wallet created!"),
        Commands::Balance { address } => println!("Balance: {:?}", address),
        Commands::Send { to, amount } => println!("Sent {} to {}", amount, to),
        Commands::History => println!("Transaction history"),
    }
}
