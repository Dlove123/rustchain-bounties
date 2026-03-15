# RustChain Wallet CLI

**Bounty**: #1752 - Native Rust Wallet for RustChain — CLI + crates.io  
**Reward**: 50-100 RTC

## Features

- ✅ Create new wallets
- ✅ Check balance via RustChain RPC
- ✅ Send RTC transactions
- ✅ View transaction history
- ✅ Export/Import private keys
- ✅ Secure key storage

## Installation

### From Source

```bash
git clone https://github.com/Dlove123/rustchain-bounties.git
cd rust-wallet-cli-1752
cargo build --release
cargo install --path .
```

### From crates.io (TODO)

```bash
cargo install rustchain-wallet
```

## Usage

```bash
# Create a new wallet
rustchain-wallet create --name mywallet

# Check balance
rustchain-wallet balance
rustchain-wallet balance --address RTCxxxxx

# Send RTC
rustchain-wallet send --to RTCxxxxx --amount 100

# View transaction history
rustchain-wallet history
rustchain-wallet history --limit 20

# Show wallet address
rustchain-wallet address

# Export private key (be careful!)
rustchain-wallet export --confirm

# Import wallet from private key
rustchain-wallet import --key <hex_key>
```

## Configuration

Wallets are stored in `~/.rustchain/wallets/`

## Security

⚠️ **Important Security Notes**:

1. Never share your private key
2. Backup your wallet file
3. Use strong passwords (future feature)
4. This is beta software - test with small amounts first

## Payment Information

**PayPal**: 979749654@qq.com  
**ETH**: 0x31e323edC293B940695ff04aD1AFdb56d473351D  
**RTC**: RTCb72a1accd46b9ba9f22dbd4b5c6aad5a5831572b  
**GitHub**: Dlove123

## License

MIT
