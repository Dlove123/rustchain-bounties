# Explorer Integration for SophiaCore Inspector
# Component 2 of 4 - 50 RTC

def display_verdict(miner_id, result):
    emoji = result.get('emoji_seal', '⚠️')
    verdict = result.get('verdict', 'CAUTIOUS')
    conf = result.get('confidence', 0.5)
    return f"{emoji} Sophia Elya Check: {verdict} ({conf*100:.0f}% confidence)"

def get_miner_status(miner_id):
    return {"miner": miner_id, "status": "inspected"}
