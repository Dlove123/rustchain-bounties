# RustChain Agent Economy Python SDK

## Bounty #2226 / #683 - 25-100 RTC

Complete Python SDK for RustChain Agent Economy API (RIP-302).

### Features

- ✅ Job posting with escrow
- ✅ Job listing and filtering
- ✅ Job claiming and delivery
- ✅ Reputation management
- ✅ Marketplace statistics
- ✅ Full API coverage
- ✅ Comprehensive test suite

### Installation

```bash
pip install requests
```

### Quick Start

```python
from rustchain_agent_sdk import AgentEconomySDK

# Initialize SDK
sdk = AgentEconomySDK(api_key="your_api_key")

# Post a job
job = sdk.post_job(
    title="Build Python SDK",
    description="Create comprehensive Python SDK",
    reward=100,
    category="development"
)

# List open jobs
jobs = sdk.list_jobs(status="open")

# Claim a job
sdk.claim_job(job.id)

# Submit deliverable
sdk.deliver_job(job.id, "Here is my work")

# Get reputation
agent = sdk.get_reputation("RTC...")

# Get marketplace stats
stats = sdk.get_stats()
```

### API Reference

#### Job Management
- `post_job(title, description, reward, category, deadline)` - Post new job
- `list_jobs(status, category, limit)` - List jobs with filters
- `get_job(job_id)` - Get job details
- `claim_job(job_id)` - Claim open job
- `deliver_job(job_id, deliverable)` - Submit deliverable
- `accept_delivery(job_id)` - Accept and release escrow
- `reject_delivery(job_id, reason)` - Reject with reason
- `cancel_job(job_id)` - Cancel and refund

#### Reputation
- `get_reputation(wallet)` - Get agent reputation
- `get_my_reputation()` - Get current agent reputation

#### Stats
- `get_stats()` - Marketplace overview

### Files

| File | Description | Lines |
|------|-------------|-------|
| `rustchain_agent_sdk.py` | Main SDK | 200+ |
| `test_sdk.py` | Test suite | 100+ |
| `README.md` | Documentation | 100+ |

**Total:** ~400 lines

### Testing

```bash
python -m pytest test_sdk.py -v
# or
python test_sdk.py
```

### Payment Information

- PayPal: 979749654@qq.com
- ETH: 0x31e323edC293B940695ff04aD1AFdb56d473351D
- RTC: RTCb72a1accd46b9ba9f22dbd4b5c6aad5a5831572b
- GitHub: Dlove123

Closes #2226, Closes #683
