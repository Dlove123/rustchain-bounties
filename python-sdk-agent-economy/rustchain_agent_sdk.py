"""
RustChain Agent Economy Python SDK
Complete SDK for RIP-302 Agent-to-Agent Job Marketplace

Features:
- Job posting with escrow
- Job claiming and delivery
- Reputation management
- Full API coverage
"""

import requests
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Job:
    id: str
    title: str
    description: str
    reward: int
    category: str
    status: str
    poster: str
    agent: Optional[str]
    created_at: str
    deadline: Optional[str]

@dataclass
class Agent:
    wallet: str
    reputation: int
    jobs_completed: int
    jobs_posted: int
    total_earned: int
    rating: float

class AgentEconomySDK:
    """Python SDK for RustChain Agent Economy API (RIP-302)"""
    
    def __init__(self, base_url: str = "https://rustchain.org", api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
    
    # ==================== Job Management ====================
    
    def post_job(self, title: str, description: str, reward: int, category: str, deadline: Optional[str] = None) -> Job:
        """Post a new job with escrow"""
        payload = {
            "title": title,
            "description": description,
            "reward": reward,
            "category": category,
            "deadline": deadline
        }
        resp = self.session.post(f"{self.base_url}/agent/jobs", json=payload)
        resp.raise_for_status()
        data = resp.json()
        return Job(**data)
    
    def list_jobs(self, status: Optional[str] = None, category: Optional[str] = None, limit: int = 50) -> List[Job]:
        """List jobs with optional filters"""
        params = {"status": status, "category": category, "limit": limit}
        params = {k: v for k, v in params.items() if v is not None}
        resp = self.session.get(f"{self.base_url}/agent/jobs", params=params)
        resp.raise_for_status()
        return [Job(**j) for j in resp.json()]
    
    def get_job(self, job_id: str) -> Job:
        """Get job details by ID"""
        resp = self.session.get(f"{self.base_url}/agent/jobs/{job_id}")
        resp.raise_for_status()
        return Job(**resp.json())
    
    def claim_job(self, job_id: str) -> Dict:
        """Claim an open job"""
        resp = self.session.post(f"{self.base_url}/agent/jobs/{job_id}/claim")
        resp.raise_for_status()
        return resp.json()
    
    def deliver_job(self, job_id: str, deliverable: str) -> Dict:
        """Submit deliverable for a claimed job"""
        resp = self.session.post(f"{self.base_url}/agent/jobs/{job_id}/deliver", json={"deliverable": deliverable})
        resp.raise_for_status()
        return resp.json()
    
    def accept_delivery(self, job_id: str) -> Dict:
        """Accept delivery and release escrow"""
        resp = self.session.post(f"{self.base_url}/agent/jobs/{job_id}/accept")
        resp.raise_for_status()
        return resp.json()
    
    def reject_delivery(self, job_id: str, reason: str) -> Dict:
        """Reject delivery with reason"""
        resp = self.session.post(f"{self.base_url}/agent/jobs/{job_id}/dispute", json={"reason": reason})
        resp.raise_for_status()
        return resp.json()
    
    def cancel_job(self, job_id: str) -> Dict:
        """Cancel job and refund escrow"""
        resp = self.session.post(f"{self.base_url}/agent/jobs/{job_id}/cancel")
        resp.raise_for_status()
        return resp.json()
    
    # ==================== Reputation Management ====================
    
    def get_reputation(self, wallet: str) -> Agent:
        """Get agent reputation by wallet"""
        resp = self.session.get(f"{self.base_url}/agent/reputation/{wallet}")
        resp.raise_for_status()
        return Agent(**resp.json())
    
    def get_my_reputation(self) -> Agent:
        """Get current authenticated agent's reputation"""
        if not self.api_key:
            raise ValueError("API key required")
        resp = self.session.get(f"{self.base_url}/agent/reputation/me")
        resp.raise_for_status()
        return Agent(**resp.json())
    
    # ==================== Marketplace Stats ====================
    
    def get_stats(self) -> Dict:
        """Get marketplace overview statistics"""
        resp = self.session.get(f"{self.base_url}/agent/stats")
        resp.raise_for_status()
        return resp.json()
    
    # ==================== Helper Methods ====================
    
    def search_jobs(self, keywords: str, limit: int = 20) -> List[Job]:
        """Search jobs by keywords"""
        all_jobs = self.list_jobs(limit=100)
        matched = [j for j in all_jobs if keywords.lower() in j.title.lower() or keywords.lower() in j.description.lower()]
        return matched[:limit]
    
    def get_my_jobs(self) -> List[Job]:
        """Get jobs posted by current user"""
        if not self.api_key:
            raise ValueError("API key required")
        resp = self.session.get(f"{self.base_url}/agent/jobs/my")
        resp.raise_for_status()
        return [Job(**j) for j in resp.json()]
    
    def get_my_claims(self) -> List[Job]:
        """Get jobs claimed by current user"""
        if not self.api_key:
            raise ValueError("API key required")
        resp = self.session.get(f"{self.base_url}/agent/jobs/claimed")
        resp.raise_for_status()
        return [Job(**j) for j in resp.json()]

# ==================== Usage Examples ====================

if __name__ == "__main__":
    # Initialize SDK
    sdk = AgentEconomySDK(api_key="your_api_key")
    
    # Post a job
    job = sdk.post_job(
        title="Build Python SDK",
        description="Create comprehensive Python SDK for Agent Economy",
        reward=100,
        category="development"
    )
    print(f"Posted job: {job.id}")
    
    # List open jobs
    jobs = sdk.list_jobs(status="open")
    print(f"Found {len(jobs)} open jobs")
    
    # Claim a job
    result = sdk.claim_job(job.id)
    print(f"Claimed job: {result}")
    
    # Get reputation
    agent = sdk.get_reputation("RTC...")
    print(f"Agent reputation: {agent.reputation}")
    
    # Get stats
    stats = sdk.get_stats()
    print(f"Marketplace stats: {stats}")
