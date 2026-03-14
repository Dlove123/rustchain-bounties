# RustChain Error Message Translations (Chinese)

Chinese translations for RustChain error messages.

## Translations

### Errors (15 messages)
- insufficient_balance → 余额不足
- invalid_address → 无效地址
- transaction_failed → 交易失败
- And more...

### Success (3 messages)
- transaction_sent → 交易已发送
- balance_updated → 余额已更新
- sync_complete → 同步完成

### Labels (6 messages)
- balance → 余额
- address → 地址
- And more...

## Usage

```python
import json

with open('translations_zh.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Get error message
error = translations['errors']['insufficient_balance']
print(error)  # 余额不足
```

## Files

- translations_zh.json - Chinese translations
- README.md - Documentation

---

Fixes #1593
