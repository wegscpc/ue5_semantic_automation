"""
Test client for Python Bridge Server

This script tests the TCP bridge connection without requiring UE5.
Use this to verify the bridge server is working correctly.
"""

import socket
import json
import time


def test_bridge_connection(host='127.0.0.1', port=55557):
    """Test connection to bridge server"""
    print(f"🔌 Connecting to bridge server at {host}:{port}...")
    
    try:
        # Create socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(5)
        
        # Connect
        client.connect((host, port))
        print("✅ Connected successfully!\n")
        
        # Test commands
        test_commands = [
            {
                'name': 'Ping Test',
                'command': 'ping',
                'params': {}
            },
            {
                'name': 'Suggest Name Test',
                'command': 'suggest_name',
                'params': {
                    'original_name': 'cube_01',
                    'asset_type': 'StaticMesh'
                }
            },
            {
                'name': 'Generate Material Test',
                'command': 'generate_material',
                'params': {
                    'description': 'shiny red metal'
                }
            },
            {
                'name': 'Generate Metadata Test',
                'command': 'generate_metadata',
                'params': {
                    'asset_name': 'SM_Chair',
                    'asset_type': 'StaticMesh'
                }
            }
        ]
        
        for test in test_commands:
            print(f"📤 Testing: {test['name']}")
            print(f"   Command: {test['command']}")
            
            # Create command
            command_data = {
                'command': test['command'],
                'params': test['params']
            }
            
            # Send command
            message = json.dumps(command_data)
            client.send(message.encode('utf-8'))
            print(f"   Sent: {message[:100]}...")
            
            # Receive response
            response = client.recv(4096)
            response_data = json.loads(response.decode('utf-8'))
            
            # Check result
            if response_data.get('success'):
                print(f"   ✅ Success!")
                print(f"   Response: {json.dumps(response_data['result'], indent=2)[:200]}...")
            else:
                print(f"   ❌ Failed: {response_data.get('error')}")
            
            print()
            time.sleep(0.5)
        
        # Close connection
        client.close()
        print("✅ All tests completed!")
        print("\n🎉 Bridge server is working correctly!")
        
        return True
        
    except ConnectionRefusedError:
        print("❌ Connection refused!")
        print("   Make sure bridge_server.py is running:")
        print("   python bridge_server.py")
        return False
        
    except socket.timeout:
        print("❌ Connection timeout!")
        print("   Bridge server is not responding")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    print("=" * 60)
    print("Python Bridge Server Test Client")
    print("=" * 60)
    print()
    
    success = test_bridge_connection()
    
    if success:
        print("\n✅ Bridge server is ready for UE5 integration!")
    else:
        print("\n❌ Bridge server test failed")
        print("   Start the server with: python bridge_server.py")
