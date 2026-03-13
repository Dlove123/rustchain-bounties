use clap::Parser;
use reqwest;
use serde::Deserialize;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Wallet address
    #[arg(short, long)]
    wallet: String,

    /// Node URL
    #[arg(short, long, default_value = "https://50.28.86.131")]
    node: String,

    /// Mining threads
    #[arg(short, long, default_value = "4")]
    threads: usize,
}

#[derive(Debug, Deserialize)]
struct EpochResponse {
    epoch: u64,
    slot: u64,
    blocks_per_epoch: u64,
    enrolled_miners: u64,
}

#[derive(Debug, Deserialize)]
struct BalanceResponse {
    amount_i64: i64,
    amount_rtc: f64,
    miner_id: String,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    println!("🦀 RustChain Miner (Rust Port)");
    println!("Wallet: {}", args.wallet);
    println!("Node: {}", args.node);
    println!("Threads: {}", args.threads);
    println!();

    // Get epoch info
    let client = reqwest::Client::new();
    let epoch_url = format!("{}/epoch", args.node);
    
    match client.get(&epoch_url).send().await {
        Ok(resp) => {
            match resp.json::<EpochResponse>().await {
                Ok(epoch) => {
                    println!("📊 Current Epoch: {}", epoch.epoch);
                    println!("📊 Current Slot: {}", epoch.slot);
                    println!("📊 Active Miners: {}", epoch.enrolled_miners);
                }
                Err(e) => eprintln!("Failed to parse epoch response: {}", e),
            }
        }
        Err(e) => eprintln!("Failed to fetch epoch: {}", e),
    }

    // Get balance
    let balance_url = format!("{}/wallet/balance?miner_id={}", args.node, args.wallet);
    
    match client.get(&balance_url).send().await {
        Ok(resp) => {
            match resp.json::<BalanceResponse>().await {
                Ok(balance) => {
                    println!("💰 Balance: {:.2} RTC", balance.amount_rtc);
                }
                Err(e) => eprintln!("Failed to parse balance response: {}", e),
            }
        }
        Err(e) => eprintln!("Failed to fetch balance: {}", e),
    }

    println!();
    println!("⛏️  Starting mining with {} threads...", args.threads);
    println!("⚠️  This is a port - actual mining logic to be implemented");

    Ok(())
}
