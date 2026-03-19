"""
Tests for RustChain Agent Economy Python SDK
"""

import unittest
from unittest.mock import Mock, patch
from rustchain_agent_sdk import AgentEconomySDK, Job, Agent

class TestAgentEconomySDK(unittest.TestCase):
    
    def setUp(self):
        self.sdk = AgentEconomySDK(base_url="https://test.rustchain.org", api_key="test_key")
    
    @patch('rustchain_agent_sdk.requests.Session.post')
    def test_post_job(self, mock_post):
        mock_post.return_value.json.return_value = {
            "id": "job123", "title": "Test Job", "description": "Test",
            "reward": 100, "category": "dev", "status": "open",
            "poster": "RTC123", "agent": None, "created_at": "2026-03-19", "deadline": None
        }
        job = self.sdk.post_job("Test", "Test desc", 100, "dev")
        self.assertEqual(job.id, "job123")
        self.assertEqual(job.reward, 100)
    
    @patch('rustchain_agent_sdk.requests.Session.get')
    def test_list_jobs(self, mock_get):
        mock_get.return_value.json.return_value = [
            {"id": "job1", "title": "Job 1", "description": "D1", "reward": 50, "category": "dev", "status": "open", "poster": "RTC1", "agent": None, "created_at": "2026-03-19", "deadline": None},
            {"id": "job2", "title": "Job 2", "description": "D2", "reward": 100, "category": "design", "status": "open", "poster": "RTC2", "agent": None, "created_at": "2026-03-19", "deadline": None}
        ]
        jobs = self.sdk.list_jobs(status="open")
        self.assertEqual(len(jobs), 2)
    
    @patch('rustchain_agent_sdk.requests.Session.get')
    def test_get_reputation(self, mock_get):
        mock_get.return_value.json.return_value = {
            "wallet": "RTC123", "reputation": 100, "jobs_completed": 10,
            "jobs_posted": 5, "total_earned": 1000, "rating": 4.5
        }
        agent = self.sdk.get_reputation("RTC123")
        self.assertEqual(agent.reputation, 100)
        self.assertEqual(agent.jobs_completed, 10)
    
    @patch('rustchain_agent_sdk.requests.Session.post')
    def test_claim_job(self, mock_post):
        mock_post.return_value.json.return_value = {"success": True, "claimed_at": "2026-03-19"}
        result = self.sdk.claim_job("job123")
        self.assertTrue(result["success"])
    
    @patch('rustchain_agent_sdk.requests.Session.post')
    def test_deliver_job(self, mock_post):
        mock_post.return_value.json.return_value = {"success": True, "delivered_at": "2026-03-19"}
        result = self.sdk.deliver_job("job123", "Here is my work")
        self.assertTrue(result["success"])
    
    @patch('rustchain_agent_sdk.requests.Session.get')
    def test_get_stats(self, mock_get):
        mock_get.return_value.json.return_value = {
            "total_jobs": 100, "open_jobs": 50, "total_volume": 10000,
            "active_agents": 25, "avg_completion_time": "2 days"
        }
        stats = self.sdk.get_stats()
        self.assertEqual(stats["total_jobs"], 100)

if __name__ == "__main__":
    unittest.main()
