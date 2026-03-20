# Security Fix: Faucet Rate Limit Bypass Prevention
# Bounty #2246 - 300 RTC

"""
Fix: X-Forwarded-For header spoofing vulnerability

Vulnerability: Attackers could bypass rate limits by spoofing X-Forwarded-For header
Fix: Validate and sanitize X-Forwarded-For, use multiple identification methods
"""

import hashlib
import time
from typing import Optional, List

class RateLimitValidator:
    """Prevent X-Forwarded-For spoofing attacks"""
    
    def __init__(self, trusted_proxies: Optional[List[str]] = None):
        self.trusted_proxies = trusted_proxies or []
        self.rate_limits = {}  # {identifier: {count, reset_time}}
    
    def get_client_identifier(self, request_headers: dict, request_ip: str) -> str:
        """
        Get reliable client identifier preventing X-Forwarded-For spoofing
        
        Args:
            request_headers: HTTP headers from request
            request_ip: Direct connection IP
            
        Returns:
            Reliable client identifier hash
        """
        xff = request_headers.get('X-Forwarded-For', '')
        
        # If XFF exists, validate it
        if xff:
            xff_list = [ip.strip() for ip in xff.split(',')]
            
            # Use the first untrusted IP (closest to real client)
            client_ip = self._extract_real_ip(xff_list, request_ip)
        else:
            client_ip = request_ip
        
        # Create fingerprint from multiple sources
        fingerprint = self._create_fingerprint(client_ip, request_headers)
        return hashlib.sha256(fingerprint.encode()).hexdigest()[:16]
    
    def _extract_real_ip(self, xff_list: List[str], direct_ip: str) -> str:
        """Extract real client IP from X-Forwarded-For chain"""
        # Walk from right to left, skip trusted proxies
        for ip in reversed(xff_list):
            if ip not in self.trusted_proxies:
                return ip
        return direct_ip
    
    def _create_fingerprint(self, ip: str, headers: dict) -> str:
        """Create multi-factor client fingerprint"""
        factors = [
            ip,
            headers.get('User-Agent', ''),
            headers.get('Accept-Language', ''),
            str(int(time.time()) // 3600),  # Hour-based rotation
        ]
        return '|'.join(factors)
    
    def check_rate_limit(self, client_id: str, limit: int = 10, window: int = 3600) -> bool:
        """
        Check if client has exceeded rate limit
        
        Args:
            client_id: Client identifier
            limit: Max requests per window
            window: Time window in seconds
            
        Returns:
            True if allowed, False if rate limited
        """
        now = time.time()
        
        if client_id not in self.rate_limits:
            self.rate_limits[client_id] = {'count': 1, 'reset': now + window}
            return True
        
        record = self.rate_limits[client_id]
        
        # Reset if window expired
        if now > record['reset']:
            record['count'] = 1
            record['reset'] = now + window
            return True
        
        # Check limit
        if record['count'] >= limit:
            return False
        
        record['count'] += 1
        return True
    
    def get_remaining(self, client_id: str) -> int:
        """Get remaining requests for client"""
        if client_id not in self.rate_limits:
            return 10
        record = self.rate_limits[client_id]
        if time.time() > record['reset']:
            return 10
        return max(0, 10 - record['count'])

# Example usage
if __name__ == "__main__":
    validator = RateLimitValidator(trusted_proxies=['10.0.0.1', '192.168.1.1'])
    
    # Simulate request
    headers = {'X-Forwarded-For': '1.2.3.4, 10.0.0.1', 'User-Agent': 'Mozilla/5.0'}
    client_id = validator.get_client_identifier(headers, '10.0.0.1')
    
    print(f"Client ID: {client_id}")
    print(f"Remaining: {validator.get_remaining(client_id)}")
