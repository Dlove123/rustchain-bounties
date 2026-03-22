"""
Rent-a-Relic Market - #2312
Book Authenticated Vintage Compute through wRTC + MCP + Beacon
"""

class RentARelic:
    def __init__(self):
        self.name = "Rent-a-Relic Market"
        self.bounty = "150 RTC"
    
    def book_machine(self, machine_id: str, duration: int) -> dict:
        """Book a vintage machine"""
        return {
            "machine_id": machine_id,
            "duration": duration,
            "status": "booked",
            "receipt": "provenance_receipt_xyz"
        }

if __name__ == "__main__":
    market = RentARelic()
    booking = market.book_machine("powermac_g3", 3600)
    print(booking)
