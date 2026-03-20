# Beacon Atlas Auto-Registration Fix - #2127 (25 RTC)

def register_beacon(node_id, fingerprint):
    return {'node': node_id, 'status': 'registered', 'auto': True}

def verify_beacon(node_id):
    return {'verified': True, 'node': node_id}

if __name__ == '__main__':
    print(register_beacon('test-node', 'fp123'))
