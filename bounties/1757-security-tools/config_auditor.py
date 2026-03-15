#!/usr/bin/env python3
"""
Security Audit Tool #3: Configuration Auditor
Check configuration files for security best practices

Bounty #1757 - Harden the Forge Security Season
"""

import os
import json
import yaml
from typing import Dict, List

class ConfigAuditor:
    """Audit configuration files for security issues"""
    
    def __init__(self):
        self.findings = []
    
    def audit_env_file(self, filename: str = ".env") -> List[Dict]:
        """Audit .env file for security issues"""
        findings = []
        
        if not os.path.exists(filename):
            return findings
        
        with open(filename, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    
                    # Check for hardcoded secrets
                    if any(secret in key.lower() for secret in ['password', 'secret', 'key', 'token']):
                        if value and not value.startswith('${'):
                            findings.append({
                                'file': filename,
                                'line': line_num,
                                'issue': f"Hardcoded secret: {key}",
                                'severity': 'high',
                                'recommendation': 'Use environment variables or secrets manager'
                            })
        
        return findings
    
    def audit_dockerfile(self, filename: str = "Dockerfile") -> List[Dict]:
        """Audit Dockerfile for security issues"""
        findings = []
        
        if not os.path.exists(filename):
            return findings
        
        with open(filename, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # Check for running as root
                if line.startswith('USER') and 'root' in line:
                    findings.append({
                        'file': filename,
                        'line': line_num,
                        'issue': 'Running as root user',
                        'severity': 'medium',
                        'recommendation': 'Create and use non-root user'
                    })
                
                # Check for latest tag
                if line.startswith('FROM') and ':latest' in line:
                    findings.append({
                        'file': filename,
                        'line': line_num,
                        'issue': 'Using :latest tag',
                        'severity': 'medium',
                        'recommendation': 'Use specific version tags'
                    })
        
        return findings
    
    def audit_github_actions(self, filename: str = ".github/workflows/ci.yml") -> List[Dict]:
        """Audit GitHub Actions workflow for security issues"""
        findings = []
        
        if not os.path.exists(filename):
            return findings
        
        try:
            with open(filename, 'r') as f:
                workflow = yaml.safe_load(f)
            
            # Check for pull_request_target
            if 'pull_request_target' in str(workflow):
                findings.append({
                    'file': filename,
                    'issue': 'Using pull_request_target trigger',
                    'severity': 'high',
                    'recommendation': 'Use pull_request instead to avoid code injection'
                })
            
            # Check for secrets in logs
            if 'set +x' not in str(workflow):
                findings.append({
                    'file': filename,
                    'issue': 'May expose secrets in logs',
                    'severity': 'low',
                    'recommendation': 'Use ::add-mask:: for secrets'
                })
        
        except Exception as e:
            findings.append({
                'file': filename,
                'issue': f'Failed to parse: {str(e)}',
                'severity': 'low'
            })
        
        return findings
    
    def generate_report(self, all_findings: List[Dict], filename: str = "config_audit_report.json"):
        """Generate audit report"""
        with open(filename, 'w') as f:
            json.dump({
                'audit_type': 'configuration_security',
                'total_findings': len(all_findings),
                'high_severity': sum(1 for f in all_findings if f.get('severity') == 'high'),
                'medium_severity': sum(1 for f in all_findings if f.get('severity') == 'medium'),
                'low_severity': sum(1 for f in all_findings if f.get('severity') == 'low'),
                'findings': all_findings
            }, f, indent=2)
        print(f"📊 Report saved to {filename}")

def main():
    auditor = ConfigAuditor()
    
    print("🔒 Security Audit Tool - Configuration Auditor")
    print("=" * 50)
    
    all_findings = []
    
    # Audit common config files
    all_findings.extend(auditor.audit_env_file())
    all_findings.extend(auditor.audit_dockerfile())
    all_findings.extend(auditor.audit_github_actions())
    
    if all_findings:
        print(f"\n⚠️  Found {len(all_findings)} security issues:")
        for finding in all_findings:
            severity = "🔴 HIGH" if finding.get('severity') == 'high' else \
                      "🟡 MEDIUM" if finding.get('severity') == 'medium' else "🟢 LOW"
            print(f"  {severity} {finding['file']}: {finding['issue']}")
    else:
        print("\n✅ No obvious configuration issues found")
    
    auditor.generate_report(all_findings)

if __name__ == '__main__':
    main()
