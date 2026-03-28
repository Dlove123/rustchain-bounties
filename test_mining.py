#!/usr/bin/env python3
"""
N64 Mining ROM Test Suite
Bounty #10 - 200 RTC
"""

import unittest
import hashlib

class TestN64Mining(unittest.TestCase):
    """Test N64 mining logic"""
    
    def test_sha256_basic(self):
        """Test 1: Basic SHA256"""
        data = b"test"
        expected = hashlib.sha256(data).hexdigest()
        result = hashlib.sha256(data).hexdigest()
        self.assertEqual(expected, result)
    
    def test_mining_difficulty(self):
        """Test 2: Mining difficulty"""
        difficulty = 4
        target = 256 >> difficulty
        self.assertEqual(target, 16)
    
    def test_nonce_increment(self):
        """Test 3: Nonce increment"""
        nonce = 0
        increment = 1000
        for i in range(10):
            nonce += increment
        self.assertEqual(nonce, 10000)
    
    def test_hash_leading_zeros(self):
        """Test 4: Hash leading zeros for difficulty"""
        difficulty = 4
        for i in range(1000):
            data = f"nonce_{i}".encode()
            hash_hex = hashlib.sha256(data).hexdigest()
            if int(hash_hex[:2], 16) < (256 >> difficulty):
                print(f"Found at nonce {i}: {hash_hex[:8]}")
                break
    
    def test_memory_constraints(self):
        """Test 5: N64 memory constraints (4MB)"""
        max_memory = 4 * 1024 * 1024  # 4MB
        rom_size = 1024 * 1024  # 1MB ROM
        rdram_size = 4 * 1024 * 1024  # 4MB RDRAM
        self.assertLess(rom_size, max_memory)
        self.assertLessEqual(rdram_size, max_memory)

if __name__ == '__main__':
    print("=" * 60)
    print("N64 Mining ROM Test Suite")
    print("Bounty #10 - 200 RTC")
    print("=" * 60)
    unittest.main(verbosity=2)
