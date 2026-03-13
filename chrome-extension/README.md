# RustChain Balance Chrome Extension

Real-time RTC balance viewer for Chrome browser.

## Features

- 💰 Real-time RTC balance display
- 🔄 Auto-refresh every 30 seconds
- 💵 USD conversion estimate
- 💾 Secure local wallet storage
- 🔔 Badge notifications

## Installation

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (top right)
3. Click "Load unpacked"
4. Select this extension folder
5. Click extension icon and enter your wallet ID

## Usage

1. Click the extension icon in Chrome toolbar
2. Enter your RustChain wallet ID
3. Click "Save & Load" to view your balance
4. Balance auto-refreshes every 30 seconds

## Permissions

- `storage` - Save wallet ID locally
- `alarms` - Auto-refresh balance
- `host_permissions` - Connect to RustChain API

## Files

- `manifest.json` - Extension configuration
- `popup.html` - Extension popup UI
- `popup.js` - Popup logic
- `background.js` - Service worker
- `icons/` - Extension icons

## License

MIT License
