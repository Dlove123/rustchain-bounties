# Bounty Verification Bot

**Bounty #747** - Auto-Verify Claims for RustChain

## Features

- Phase 1: Star/Follow Verification (30 RTC)
- Phase 2: Wallet Existence Check (+10 RTC)
- Phase 3: Article/URL Verification (+10 RTC)
- Phase 4: Duplicate Detection (+15 RTC)

## Usage

```bash
# Set environment variables
export GITHUB_TOKEN=your_token

# Run verification
python verification_bot.py
```

## Payment Info

**PayPal**: 979749654@qq.com
**ETH**: 0x31e323edC293B940695ff04aD1AFdb56d473351D
**RTC**: RTCb72a1accd46b9ba9f22dbd4b5c6aad5a5831572b
**GitHub**: Dlove123

## New Features (v1.1)

### MelvinBot Auto-Reply
- Automatically detect MelvinBot payment reminders
- Auto-reply with contributor information
- Ensure timely payment processing

### Configuration Generator
- Generate .env.example template
- Generate payment_config.json
- Easy setup for new users

## Usage

```bash
# Generate configuration
python config_generator.py

# Run verification bot
python verification_bot.py

# Run MelvinBot auto-responder
python -c "from verification_bot import main_with_melvinbot; main_with_melvinbot()"

# Run tests
python -m pytest test_*.py
```
