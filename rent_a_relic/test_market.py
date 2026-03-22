"""
Tests for Rent-a-Relic Market - #2312
"""
import pytest
from market import RentARelic

class TestRentARelic:
    def test_init(self):
        market = RentARelic()
        assert market.name == "Rent-a-Relic Market"
    
    def test_book_machine(self):
        market = RentARelic()
        booking = market.book_machine("g3", 3600)
        assert booking["status"] == "booked"
        assert "machine_id" in booking

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
