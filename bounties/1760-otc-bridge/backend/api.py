#!/usr/bin/env python3
"""
OTC Bridge Backend API
Order matching and swap execution

Bounty #1760 - OTC Bridge - RTC Swap Page
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# In-memory order book (use database in production)
orders = []
order_id = 0

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Get all active orders"""
    active_orders = [o for o in orders if o['status'] == 'active']
    return jsonify({
        'success': True,
        'orders': active_orders,
        'count': len(active_orders)
    })

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create a new swap order"""
    global order_id
    
    data = request.json
    if not all(k in data for k in ['type', 'amount', 'price']):
        return jsonify({'success': False, 'error': 'Missing fields'}), 400
    
    order = {
        'id': order_id,
        'type': data['type'],  # 'buy' or 'sell'
        'amount': float(data['amount']),
        'price': float(data['price']),
        'status': 'active',
        'created_at': datetime.now().isoformat(),
        'user_address': data.get('user_address', '')
    }
    
    orders.append(order)
    order_id += 1
    
    return jsonify({
        'success': True,
        'order_id': order['id'],
        'message': 'Order created'
    }), 201

@app.route('/api/orders/<int:order_id>/fill', methods=['POST'])
def fill_order(order_id):
    """Fill an existing order"""
    order = next((o for o in orders if o['id'] == order_id), None)
    if not order:
        return jsonify({'success': False, 'error': 'Order not found'}), 404
    
    if order['status'] != 'active':
        return jsonify({'success': False, 'error': 'Order not active'}), 400
    
    data = request.json
    order['status'] = 'completed'
    order['filled_at'] = datetime.now().isoformat()
    order['filled_by'] = data.get('user_address', '')
    
    return jsonify({
        'success': True,
        'message': 'Order filled',
        'tx_hash': '0x' + 'abcd1234'  # Mock transaction hash
    })

@app.route('/api/price', methods=['GET'])
def get_price():
    """Get current RTC/ETH exchange rate"""
    # In production: fetch from oracle or DEX
    return jsonify({
        'success': True,
        'price': 0.10,  # 1 RTC = 0.10 ETH
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get bridge statistics"""
    total_volume = sum(o['amount'] for o in orders if o['status'] == 'completed')
    return jsonify({
        'success': True,
        'total_orders': len(orders),
        'active_orders': len([o for o in orders if o['status'] == 'active']),
        'completed_orders': len([o for o in orders if o['status'] == 'completed']),
        'total_volume_rtc': total_volume,
        'total_volume_eth': total_volume * 0.10
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
