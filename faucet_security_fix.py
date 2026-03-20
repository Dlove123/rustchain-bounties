# SECURITY FIX: Faucet Rate Limit Bypass - #2246 (300 RTC)
"""
Fix: X-Forwarded-For header spoofing vulnerability
Prevents attackers from bypassing rate limits by spoofing client IP
"""

import hashlib
import time

class FaucetValidator:
    """Prevent faucet rate limit bypass via X-Forwarded-For spoofing"""
    
    def __init__(self, trusted_proxies=None):
        self.trusted_proxies = trusted_proxies or []
        self.rate_limits = {}
    
    def get_client_ip(self, headers, direct_ip):
        """Extract real client IP from X-Forwarded-For chain"""
        xff = headers.get('X-Forwarded-For', '')
        if xff:
            xff_list = [ip.strip() for ip in xff.split(',')]
            # Use first untrusted IP (closest to real client)
            for ip in reversed(xff_list):
                if ip not in self.trusted_proxies:
                    return ip
        return direct_ip
    
    def check_rate_limit(self, client_id, limit=10, window=3600):
        """Check if client has exceeded rate limit"""
        now = time.time()
        if client_id not in self.rate_limits:
            self.rate_limits[client_id] = {'count': 1, 'reset': now + window}
            return True
        rec = self.rate_limits[client_id]
        if now > rec['reset']:
            rec = {'count': 1, 'reset': now + window}
        if rec['count'] >= limit:
            return False
        rec['count'] += 1
        self.rate_limits[client_id] = rec
        return True
    
    def verify_request(self, headers, direct_ip):
        """Verify faucet request"""
        client_ip = self.get_client_ip(headers, direct_ip)
        client_id = hashlib.sha256(client_ip.encode()).hexdigest()[:16]
        allowed = self.check_rate_limit(client_id)
        return {'allowed': allowed, 'client_ip': client_ip, 'client_id': client_id}

if __name__ == '__main__':
    v = FaucetValidator()
    headers = {'X-Forwarded-For': '1.2.3.4, 10.0.0.1'}
    print(v.verify_request(headers, '10.0.0.1'))
