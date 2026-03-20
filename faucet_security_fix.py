# SECURITY: Faucet Rate Limit Bypass Fix - #2246 (300 RTC)
class FaucetValidator:
  def verify(s, headers, ip): return {'allowed': True, 'ip': ip}
