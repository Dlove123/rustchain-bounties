#!/usr/bin/env python3
"""
Cross-Repo Star & Engagement Tool
Track and manage stars across RustChain ecosystem

Bounty #1758 - Cross-Repo Star & Engage Multiplier
"""

import requests
from typing import List, Dict
from datetime import datetime

class CrossRepoStar:
    """Manage stars across multiple repos"""
    
    def __init__(self, github_token: str):
        self.token = github_token
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        })
        self.base_url = 'https://api.github.com'
    
    def get_user(self) -> Dict:
        """Get current user info"""
        response = self.session.get(f'{self.base_url}/user')
        if response.status_code == 200:
            return response.json()
        return {}
    
    def star_repo(self, owner: str, repo: str) -> bool:
        """Star a repository"""
        url = f'{self.base_url}/user/starred/{owner}/{repo}'
        response = self.session.put(url)
        return response.status_code == 204
    
    def unstar_repo(self, owner: str, repo: str) -> bool:
        """Unstar a repository"""
        url = f'{self.base_url}/user/starred/{owner}/{repo}'
        response = self.session.delete(url)
        return response.status_code == 204
    
    def check_starred(self, owner: str, repo: str) -> bool:
        """Check if repo is starred"""
        url = f'{self.base_url}/user/starred/{owner}/{repo}'
        response = self.session.get(url)
        return response.status_code == 204
    
    def get_starred_repos(self) -> List[Dict]:
        """Get all starred repos"""
        repos = []
        page = 1
        while True:
            response = self.session.get(
                f'{self.base_url}/user/starred',
                params={'per_page': 100, 'page': page}
            )
            if response.status_code == 200:
                data = response.json()
                if not data:
                    break
                repos.extend(data)
                page += 1
            else:
                break
        return repos
    
    def star_ecosystem(self, org: str = 'Scottcjn') -> Dict:
        """Star all repos in an organization"""
        response = self.session.get(
            f'{self.base_url}/orgs/{org}/repos',
            params={'per_page': 100}
        )
        
        if response.status_code != 200:
            return {'success': False, 'error': 'Failed to fetch repos'}
        
        repos = response.json()
        starred = 0
        already_starred = 0
        failed = 0
        
        for repo in repos:
            repo_name = repo['name']
            if self.check_starred(org, repo_name):
                already_starred += 1
                print(f"✅ Already starred: {org}/{repo_name}")
            elif self.star_repo(org, repo_name):
                starred += 1
                print(f"⭐ Starred: {org}/{repo_name}")
            else:
                failed += 1
                print(f"❌ Failed: {org}/{repo_name}")
        
        return {
            'success': True,
            'starred': starred,
            'already_starred': already_starred,
            'failed': failed,
            'total': len(repos)
        }
    
    def calculate_engagement_score(self) -> Dict:
        """Calculate engagement multiplier score"""
        starred = self.get_starred_repos()
        
        # Count RustChain ecosystem stars
        ecosystem_count = sum(
            1 for repo in starred 
            if repo.get('owner', {}).get('login') in ['Scottcjn', 'RustChain-labs']
        )
        
        # Calculate multiplier
        if ecosystem_count >= 100:
            multiplier = 3.0
            badge = 'Star King'
        elif ecosystem_count >= 50:
            multiplier = 2.0
            badge = 'Super Star'
        elif ecosystem_count >= 20:
            multiplier = 1.5
            badge = 'Active Supporter'
        elif ecosystem_count >= 10:
            multiplier = 1.2
            badge = 'Supporter'
        else:
            multiplier = 1.0
            badge = 'Beginner'
        
        return {
            'total_starred': len(starred),
            'ecosystem_stars': ecosystem_count,
            'multiplier': multiplier,
            'badge': badge,
            'calculated_at': datetime.now().isoformat()
        }
    
    def generate_report(self, output_file: str = 'engagement_report.json'):
        """Generate engagement report"""
        import json
        score = self.calculate_engagement_score()
        
        with open(output_file, 'w') as f:
            json.dump(score, f, indent=2)
        
        print(f"📊 Report saved to {output_file}")
        return score

def main():
    print("⭐ Cross-Repo Star & Engagement Tool")
    print("=" * 50)
    
    import os
    token = os.getenv('GITHUB_TOKEN', '')
    
    if not token:
        print("⚠️  Please set GITHUB_TOKEN environment variable")
        return
    
    tool = CrossRepoStar(token)
    
    # Get user info
    user = tool.get_user()
    if user:
        print(f"\n👤 Logged in as: {user.get('login')}")
    
    # Calculate engagement score
    print("\n📊 Calculating engagement score...")
    score = tool.generate_report()
    
    print(f"\nTotal Starred: {score['total_starred']}")
    print(f"Ecosystem Stars: {score['ecosystem_stars']}")
    print(f"Multiplier: {score['multiplier']}x")
    print(f"Badge: {score['badge']}")

if __name__ == '__main__':
    main()
