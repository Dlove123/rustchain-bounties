#!/usr/bin/env python3
"""
Test suite for MelvinBot auto-responder
"""

import unittest
from verification_bot import MelvinBotResponder

class TestMelvinBotResponder(unittest.TestCase):
    
    def test_responder_initialization(self):
        """Test responder can be initialized"""
        responder = MelvinBotResponder('fake_token')
        self.assertIsNotNone(responder.session)
    
    def test_reply_format(self):
        """Test reply format is correct"""
        expected_keywords = ['Upwork', 'PayPal', 'GitHub', '979749654@qq.com', 'Dlove123']
        reply = """## 🙋 Contributor Information
**Upwork**: [Your Upwork ID]
**PayPal**: 979749654@qq.com
**GitHub**: Dlove123"""
        
        for keyword in expected_keywords:
            self.assertIn(keyword, reply)

if __name__ == '__main__':
    unittest.main()
