import React, { useState } from 'react';

/**
 * OTC Bridge Swap Interface
 * Bounty #1760 - RTC Swap Page
 */

const SwapInterface = () => {
  const [fromAmount, setFromAmount] = useState('');
  const [toAmount, setToAmount] = useState('');
  const [exchangeRate, setExchangeRate] = useState(0.10); // RTC to ETH
  const [loading, setLoading] = useState(false);

  const handleSwap = async () => {
    setLoading(true);
    try {
      // Connect wallet and execute swap
      if (window.ethereum) {
        const accounts = await window.ethereum.request({ 
          method: 'eth_requestAccounts' 
        });
        console.log('Connected:', accounts[0]);
        
        // Call smart contract
        // In production: integrate with web3.js/ethers.js
      }
    } catch (error) {
      console.error('Swap failed:', error);
    }
    setLoading(false);
  };

  const calculateToAmount = (amount) => {
    return (parseFloat(amount) * exchangeRate).toFixed(6);
  };

  return (
    <div className="swap-container">
      <h1>🌉 OTC Bridge - RTC Swap</h1>
      
      <div className="swap-card">
        <div className="input-group">
          <label>From (RTC)</label>
          <input
            type="number"
            value={fromAmount}
            onChange={(e) => {
              setFromAmount(e.target.value);
              setToAmount(calculateToAmount(e.target.value));
            }}
            placeholder="0.00"
          />
        </div>
        
        <div className="exchange-rate">
          ↓ Rate: 1 RTC = {exchangeRate} ETH ↓
        </div>
        
        <div className="input-group">
          <label>To (ETH)</label>
          <input
            type="number"
            value={toAmount}
            readOnly
            placeholder="0.00"
          />
        </div>
        
        <button 
          onClick={handleSwap}
          disabled={loading || !fromAmount}
          className="swap-button"
        >
          {loading ? 'Swapping...' : 'Swap Now'}
        </button>
        
        <div className="swap-info">
          <p>Minimum: 10 RTC</p>
          <p>Maximum: 10,000 RTC</p>
          <p>Fee: 0.5%</p>
        </div>
      </div>
      
      <style jsx>{`
        .swap-container {
          max-width: 500px;
          margin: 50px auto;
          padding: 20px;
        }
        .swap-card {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          border-radius: 20px;
          padding: 30px;
          color: white;
        }
        .input-group {
          margin: 20px 0;
        }
        .input-group label {
          display: block;
          margin-bottom: 8px;
          font-size: 14px;
        }
        .input-group input {
          width: 100%;
          padding: 15px;
          border: none;
          border-radius: 10px;
          font-size: 18px;
          box-sizing: border-box;
        }
        .exchange-rate {
          text-align: center;
          padding: 10px;
          background: rgba(255,255,255,0.2);
          border-radius: 10px;
        }
        .swap-button {
          width: 100%;
          padding: 15px;
          background: white;
          color: #667eea;
          border: none;
          border-radius: 10px;
          font-size: 18px;
          font-weight: bold;
          cursor: pointer;
          margin-top: 20px;
        }
        .swap-button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }
        .swap-info {
          margin-top: 20px;
          font-size: 12px;
          opacity: 0.8;
        }
      `}</style>
    </div>
  );
};

export default SwapInterface;
