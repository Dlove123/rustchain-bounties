#!/usr/bin/env python3
"""
Security Audit Tool #2: API Security Tester
Test API endpoints for common vulnerabilities

Bounty #1757 - Harden the Forge Security Season
"""

import requests
from typing import Dict, List

class APISecurityTester:
    """Test API endpoints for security issues"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_cors(self) -> Dict:
        """Test CORS configuration"""
        try:
            response = self.session.options(
                self.base_url,
                headers={'Origin': 'https://evil.com'}
            )
            cors_header = response.headers.get('Access-Control-Allow-Origin', '')
            return {
                'test': 'CORS',
                'passed': cors_header != '*' and 'evil.com' not in cors_header,
                'details': f"Access-Control-Allow-Origin: {cors_header}"
            }
        except Exception as e:
            return {'test': 'CORS', 'passed': False, 'error': str(e)}
    
    def test_security_headers(self) -> List[Dict]:
        """Test security headers"""
        try:
            response = self.session.get(self.base_url, timeout=10)
            headers = response.headers
            
            tests = [
                {'name': 'X-Frame-Options', 'required': True},
                {'name': 'X-Content-Type-Options', 'required': True},
                {'name': 'X-XSS-Protection', 'required': True},
                {'name': 'Strict-Transport-Security', 'required': True},
                {'name': 'Content-Security-Policy', 'required': False},
            ]
            
            results = []
            for test in tests:
                present = test['name'] in headers
                results.append({
                    'test': test['name'],
                    'passed': present or not test['required'],
                    'details': headers.get(test['name', 'MISSING'])
                })
            
            return results
        except Exception as e:
            return [{'test': 'Security Headers', 'passed': False, 'error': str(e)}]
    
    def test_rate_limiting(self) -> Dict:
        """Test for rate limiting"""
        try:
            responses = []
            for i in range(10):
                response = self.session.get(self.base_url, timeout=10)
                responses.append(response.status_code)
            
            # Check if any 429 (Too Many Requests)
            rate_limited = 429 in responses
            return {
                'test': 'Rate Limiting',
                'passed': rate_limited,
                'details': f"Status codes: {set(responses)}"
            }
        except Exception as e:
            return {'test': 'Rate Limiting', 'passed': False, 'error': str(e)}
    
    def run_all_tests(self) -> Dict:
        """Run all security tests"""
        results = {
            'url': self.base_url,
            'cors': self.test_cors(),
            'security_headers': self.test_security_headers(),
            'rate_limiting': self.test_rate_limiting(),
            'passed': 0,
            'failed': 0
        }
        
        # Count passed/failed
        if results['cors']['passed']:
            results['passed'] += 1
        else:
            results['failed'] += 1
        
        for header_test in results['security_headers']:
            if header_test['passed']:
                results['passed'] += 1
            else:
                results['failed'] += 1
        
        if results['rate_limiting']['passed']:
            results['passed'] += 1
        else:
            results['failed'] += 1
        
        return results

def main():
    print("🔒 Security Audit Tool - API Security Tester")
    print("=" * 50)
    
    # Test RustChain API
    tester = APISecurityTester("https://50.28.86.131")
    results = tester.run_all_tests()
    
    print(f"\nURL: {results['url']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    
    print(f"\n📊 CORS: {'✅' if results['cors']['passed'] else '❌'}")
    print(f"📊 Security Headers: {[h['name'] for h in results['security_headers'] if h['passed']]}")
    print(f"📊 Rate Limiting: {'✅' if results['rate_limiting']['passed'] else '❌'}")

if __name__ == '__main__':
    main()
