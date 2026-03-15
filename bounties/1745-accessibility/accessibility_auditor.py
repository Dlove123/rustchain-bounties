#!/usr/bin/env python3
"""
Accessibility Audit Tool
WCAG 2.1 compliance checker for websites

Bounty #1745 - Accessibility Issue Report
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import re

class AccessibilityAuditor:
    """Audit website for accessibility issues"""
    
    def __init__(self, url: str):
        self.url = url
        self.issues = []
        self.html = None
        self.soup = None
    
    def fetch_page(self) -> bool:
        """Fetch the webpage"""
        try:
            response = requests.get(self.url, timeout=10)
            if response.status_code == 200:
                self.html = response.text
                self.soup = BeautifulSoup(self.html, 'html.parser')
                return True
        except Exception as e:
            self.issues.append({
                'severity': 'critical',
                'issue': f'Failed to fetch page: {str(e)}'
            })
        return False
    
    def check_alt_text(self) -> List[Dict]:
        """Check for missing alt text on images"""
        issues = []
        if not self.soup:
            return issues
        
        images = self.soup.find_all('img')
        for img in images:
            alt = img.get('alt')
            if alt is None:
                issues.append({
                    'severity': 'high',
                    'wcag': '1.1.1 Non-text Content',
                    'issue': f'Image missing alt text: {img.get("src", "unknown")}',
                    'recommendation': 'Add descriptive alt attribute'
                })
            elif alt.strip() == '':
                issues.append({
                    'severity': 'medium',
                    'wcag': '1.1.1 Non-text Content',
                    'issue': 'Image has empty alt text',
                    'recommendation': 'Add descriptive alt or use alt="" for decorative images'
                })
        
        return issues
    
    def check_color_contrast(self) -> List[Dict]:
        """Check color contrast ratios"""
        # Simplified check - in production use actual contrast calculation
        issues = []
        if not self.soup:
            return issues
        
        # Check for inline styles with potential contrast issues
        elements = self.soup.find_all(style=True)
        for elem in elements:
            style = elem.get('style', '')
            if 'color:' in style and 'background' not in style:
                issues.append({
                    'severity': 'low',
                    'wcag': '1.4.3 Contrast (Minimum)',
                    'issue': 'Element has color style without background',
                    'recommendation': 'Ensure sufficient contrast ratio (4.5:1 for normal text)'
                })
        
        return issues
    
    def check_heading_structure(self) -> List[Dict]:
        """Check heading hierarchy"""
        issues = []
        if not self.soup:
            return issues
        
        headings = []
        for i in range(1, 7):
            headings.extend(self.soup.find_all(f'h{i}'))
        
        if headings:
            # Check if h1 exists
            h1s = self.soup.find_all('h1')
            if len(h1s) == 0:
                issues.append({
                    'severity': 'high',
                    'wcag': '1.3.1 Info and Relationships',
                    'issue': 'No h1 heading found',
                    'recommendation': 'Add exactly one h1 per page'
                })
            elif len(h1s) > 1:
                issues.append({
                    'severity': 'medium',
                    'wcag': '1.3.1 Info and Relationships',
                    'issue': f'Multiple h1 headings found ({len(h1s)})',
                    'recommendation': 'Use only one h1 per page'
                })
        
        return issues
    
    def check_keyboard_navigation(self) -> List[Dict]:
        """Check keyboard accessibility"""
        issues = []
        if not self.soup:
            return issues
        
        # Check for interactive elements without tabindex
        interactive = self.soup.find_all(['button', 'a', 'input', 'select'])
        for elem in interactive:
            if elem.get('onclick') and not elem.get('tabindex'):
                issues.append({
                    'severity': 'medium',
                    'wcag': '2.1.1 Keyboard',
                    'issue': 'Interactive element may not be keyboard accessible',
                    'recommendation': 'Add tabindex="0" and keyboard event handlers'
                })
        
        return issues
    
    def check_form_labels(self) -> List[Dict]:
        """Check form inputs have labels"""
        issues = []
        if not self.soup:
            return issues
        
        inputs = self.soup.find_all('input')
        for inp in inputs:
            input_id = inp.get('id')
            input_type = inp.get('type', 'text')
            
            # Skip hidden and submit buttons
            if input_type in ['hidden', 'submit', 'button']:
                continue
            
            # Check for associated label
            if input_id:
                label = self.soup.find('label', attrs={'for': input_id})
                if not label:
                    issues.append({
                        'severity': 'high',
                        'wcag': '1.3.1 Info and Relationships',
                        'issue': f'Form input missing label: {input_id}',
                        'recommendation': 'Add <label for="..."> or aria-label'
                    })
            elif not inp.get('aria-label') and not inp.get('placeholder'):
                issues.append({
                    'severity': 'high',
                    'wcag': '1.3.1 Info and Relationships',
                    'issue': 'Form input missing label or aria-label',
                    'recommendation': 'Add label, aria-label, or placeholder'
                })
        
        return issues
    
    def run_full_audit(self) -> Dict:
        """Run complete accessibility audit"""
        if not self.fetch_page():
            return {
                'url': self.url,
                'success': False,
                'issues': self.issues
            }
        
        # Run all checks
        self.issues.extend(self.check_alt_text())
        self.issues.extend(self.check_color_contrast())
        self.issues.extend(self.check_heading_structure())
        self.issues.extend(self.check_keyboard_navigation())
        self.issues.extend(self.check_form_labels())
        
        # Count by severity
        severity_count = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }
        for issue in self.issues:
            sev = issue.get('severity', 'low')
            severity_count[sev] = severity_count.get(sev, 0) + 1
        
        return {
            'url': self.url,
            'success': True,
            'total_issues': len(self.issues),
            'by_severity': severity_count,
            'issues': self.issues
        }
    
    def generate_report(self, output_file: str = 'accessibility_report.json'):
        """Generate JSON report"""
        import json
        results = self.run_full_audit()
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"📊 Report saved to {output_file}")
        return results

def main():
    print("♿ Accessibility Audit Tool")
    print("=" * 50)
    
    # Audit BoTTube UI
    url = "https://bottube.ai"
    print(f"\nAuditing: {url}")
    
    auditor = AccessibilityAuditor(url)
    results = auditor.generate_report()
    
    if results['success']:
        print(f"\n✅ Audit complete!")
        print(f"Total Issues: {results['total_issues']}")
        print(f"  🔴 Critical: {results['by_severity']['critical']}")
        print(f"  🟠 High: {results['by_severity']['high']}")
        print(f"  🟡 Medium: {results['by_severity']['medium']}")
        print(f"  🟢 Low: {results['by_severity']['low']}")
    else:
        print("\n❌ Audit failed")
        for issue in results['issues']:
            print(f"  - {issue['issue']}")

if __name__ == '__main__':
    main()
