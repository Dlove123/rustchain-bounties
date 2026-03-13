# RustChain API Postman Collection

Complete Postman collection for testing RustChain blockchain API.

## Import Collection

1. Open Postman
2. Click "Import"
3. Select `RustChain_API.postman_collection.json`
4. Collection imported successfully!

## Available Endpoints

### 1. Health
- **GET** `/health` - Check node health status

### 2. Epoch
- **GET** `/epoch` - Get current epoch information

### 3. Miners
- **GET** `/api/miners` - List active miners

### 4. Wallet Balance
- **GET** `/wallet/balance?miner_id=YOUR_ID` - Check wallet balance

### 5. Attestation
- **POST** `/attest/challenge` - Get attestation challenge
- **POST** `/attest/submit` - Submit attestation

## Environment Variable

Set `base_url` variable to your RustChain node URL.

Default: `https://50.28.86.131`

## Quick Start

1. Import collection
2. Set your miner ID in Wallet Balance request
3. Click "Send" to test
4. View response in Postman

## License

MIT License
