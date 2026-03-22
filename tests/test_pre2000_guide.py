"""
Tests for Pre-2000 Hardware Mining Guide

Validates documentation completeness and accuracy.
"""

import os
import pytest

DOC_PATH = "docs/pre2000_hardware_mining.md"


class TestPre2000HardwareGuide:
    """Test suite for vintage hardware mining guide"""
    
    def test_guide_exists(self):
        """Test that guide exists"""
        assert os.path.exists(DOC_PATH), f"Guide {DOC_PATH} not found"
    
    def test_guide_has_content(self):
        """Test guide has substantial content"""
        with open(DOC_PATH, 'r') as f:
            content = f.read()
        assert len(content) > 2000, "Guide too short"
    
    def test_has_multiple_systems(self):
        """Test multiple vintage systems are documented"""
        with open(DOC_PATH, 'r') as f:
            content = f.read()
        systems = ["G3", "G4", "BeBox", "Aptiva"]
        for system in systems:
            assert system in content, f"Missing system: {system}"
    
    def test_has_benchmarks(self):
        """Test benchmark results are included"""
        with open(DOC_PATH, 'r') as f:
            content = f.read()
        assert "Benchmark" in content or "Hash Rate" in content
    
    def test_has_setup_guide(self):
        """Test setup instructions are included"""
        with open(DOC_PATH, 'r') as f:
            content = f.read()
        assert "Setup" in content or "Install" in content
    
    def test_has_code_examples(self):
        """Test code examples are present"""
        with open(DOC_PATH, 'r') as f:
            content = f.read()
        assert "```" in content, "No code blocks found"
    
    def test_has_payment_info(self):
        """Test payment information is included"""
        with open(DOC_PATH, 'r') as f:
            content = f.read()
        assert "Payment" in content or "RTC" in content
    
    def test_tips_section(self):
        """Test tips section exists"""
        with open(DOC_PATH, 'r') as f:
            content = f.read()
        assert "Tips" in content or "Tip" in content


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
