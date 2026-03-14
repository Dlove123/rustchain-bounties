# RustChain Error Messages - Chinese Translation

## Translated Errors

| English | 中文 |
|---------|------|
| insufficient_balance | 余额不足 |
| invalid_address | 无效地址 |
| transaction_failed | 交易失败 |
| network_error | 网络错误 |
| node_unavailable | 节点不可用 |
| sync_in_progress | 同步进行中 |
| invalid_amount | 无效金额 |
| duplicate_transaction | 重复交易 |
| gas_too_low | Gas 太低 |
| nonce_too_low | Nonce 太低 |

## Usage

```json
import errors from './errors_zh_CN.json';
console.log(errors.errors.insufficient_balance); // "余额不足"
```

---

Fixes #1593
