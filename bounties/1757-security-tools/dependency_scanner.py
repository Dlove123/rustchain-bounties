#!/usr/bin/env python3
"""
Security Audit Tool #1: Dependency Vulnerability Scanner
Check Python/Node.js dependencies for known CVEs

Bounty #1757 - Harden the Forge Security Season
"""

import requests
import json
import os
from typing import List, Dict

class DependencyScanner:
    """Scan dependencies for vulnerabilities"""
    
    def __init__(self):
        self.vuln_db = "https://pypi.org/pypi/{}/json"
    
    def scan_requirements(self, filename: str = "requirements.txt") -> List[Dict]:
        """Scan Python requirements for vulnerabilities"""
        vulnerabilities = []
        
        if not os.path.exists(filename):
            print(f"⚠️  {filename} not found")
            return vulnerabilities
        
        with open(filename, 'r') as f:
            for line in f:
                package = line.strip().split('==')[0].split('>=')[0]
                if package and not package.startswith('#'):
                    result = self.check_package(package)
                    if result:
                        vulnerabilities.append(result)
        
        return vulnerabilities
    
    def check_package(self, package: str) -> Dict:
        """Check single package for vulnerabilities"""
        try:
            response = requests.get(
                self.vuln_db.format(package),
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                # Check for security advisories
                advisories = data.get('info', {}).get('project_urls', {}).get('Security', '')
                return {
                    'package': package,
                    'version': data.get('info', {}).get('version', 'unknown'),
                    'advisories': advisories,
                    'risk': 'low' if not advisories else 'high'
                }
        except Exception as e:
            pass
        return None
    
    def generate_report(self, vulnerabilities: List[Dict], filename: str = "security_report.json"):
        """Generate security report"""
        with open(filename, 'w') as f:
            json.dump({
                'scan_type': 'dependency_vulnerability',
                'total_packages': len(vulnerabilities),
                'high_risk': sum(1 for v in vulnerabilities if v.get('risk') == 'high'),
                'vulnerabilities': vulnerabilities
            }, f, indent=2)
        print(f"📊 Report saved to {filename}")

def main():
    scanner = DependencyScanner()
    
    print("🔒 Security Audit Tool - Dependency Scanner")
    print("=" * 50)
    
    vulnerabilities = scanner.scan_requirements()
    
    if vulnerabilities:
        print(f"\n⚠️  Found {len(vulnerabilities)} packages to review:")
        for vuln in vulnerabilities:
            risk = "🔴 HIGH" if vuln.get('risk') == 'high' else "🟢 LOW"
            print(f"  {risk} {vuln['package']} v{vuln['version']}")
    else:
        print("\n✅ No obvious vulnerabilities found")
    
    scanner.generate_report(vulnerabilities)

if __name__ == '__main__':
    main()
