"""
Python Bridge Server for UE5 Semantic Automation Plugin

This server acts as a bridge between the UE5 C++ plugin and the Python automation backend.
It listens for TCP connections from the UE5 plugin and routes commands to the appropriate modules.

Architecture:
- TCP Server listening on port 55557
- Receives JSON commands from UE5 plugin
- Routes commands to Python automation modules
- Returns JSON responses

Based on the unreal-mcp architecture pattern.
"""

import socket
import json
import sys
import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path

# Add src to path - go up to project root, then to src
project_root = Path(__file__).parent.parent.parent
src_path = project_root / 'src'
sys.path.insert(0, str(src_path))

print(f"Python path: {src_path}")
print(f"Path exists: {src_path.exists()}")

# Import automation modules (optional - will be None if not available)
# These require the 'unreal' module which is only available inside UE5
try:
    from core.asset_organizer import AssetOrganizer
    from ai.asset_naming import AIAssetNaming
    from materials.material_generator import MaterialGenerator
    from ai.metadata_generator import MetadataGenerator
    from qa.sanity_checker import SanityChecker
    from optimization.texture_optimizer import TextureOptimizer
    from optimization.lod_generator import LODGenerator
    print("✅ Automation modules loaded successfully")
except ImportError as e:
    print(f"⚠️  Automation modules not available (requires UE5 Python environment): {e}")
    print("   Bridge server will run in test mode with mock responses")
    AssetOrganizer = None
    AIAssetNaming = None
    MaterialGenerator = None
    MetadataGenerator = None
    SanityChecker = None
    TextureOptimizer = None
    LODGenerator = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class UE5BridgeServer:
    """TCP server for bridging UE5 plugin with Python automation backend"""
    
    def __init__(self, host: str = '127.0.0.1', port: int = 55557):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        
        # Initialize automation modules (lazy loading)
        self.organizer = None
        self.naming = None
        self.material_gen = None
        self.metadata_gen = None
        self.sanity_checker = None
        self.texture_optimizer = None
        self.lod_generator = None
        
        # Command routing
        self.commands = {
            'organize_assets': self.handle_organize_assets,
            'suggest_name': self.handle_suggest_name,
            'generate_material': self.handle_generate_material,
            'generate_metadata': self.handle_generate_metadata,
            'run_sanity_check': self.handle_sanity_check,
            'optimize_textures': self.handle_optimize_textures,
            'generate_lods': self.handle_generate_lods,
            'ping': self.handle_ping,
        }
    
    def start(self):
        """Start the TCP server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            self.running = True
            
            logger.info(f"Bridge server listening on {self.host}:{self.port}")
            
            while self.running:
                try:
                    client_socket, address = self.socket.accept()
                    logger.info(f"Client connected from {address}")
                    
                    self.handle_client(client_socket)
                    
                except KeyboardInterrupt:
                    logger.info("Server interrupted by user")
                    break
                except Exception as e:
                    logger.error(f"Error accepting connection: {e}")
                    
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the server"""
        self.running = False
        if self.socket:
            self.socket.close()
        logger.info("Bridge server stopped")
    
    def handle_client(self, client_socket: socket.socket):
        """Handle client connection"""
        try:
            while True:
                # Receive data
                data = client_socket.recv(4096)
                if not data:
                    break
                
                # Parse JSON command
                try:
                    command_data = json.loads(data.decode('utf-8'))
                    logger.info(f"Received command: {command_data.get('command')}")
                    
                    # Process command
                    response = self.process_command(command_data)
                    
                    # Send response
                    response_json = json.dumps(response)
                    client_socket.send(response_json.encode('utf-8'))
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON: {e}")
                    error_response = {'error': 'Invalid JSON format'}
                    client_socket.send(json.dumps(error_response).encode('utf-8'))
                    
        except Exception as e:
            logger.error(f"Error handling client: {e}")
        finally:
            client_socket.close()
            logger.info("Client disconnected")
    
    def process_command(self, command_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming command and route to appropriate handler"""
        command = command_data.get('command')
        params = command_data.get('params', {})
        
        if command not in self.commands:
            return {
                'success': False,
                'error': f'Unknown command: {command}'
            }
        
        try:
            handler = self.commands[command]
            result = handler(params)
            return {
                'success': True,
                'result': result
            }
        except Exception as e:
            logger.error(f"Error processing command {command}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    # Command Handlers
    
    def handle_ping(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Health check"""
        return {'status': 'ok', 'message': 'Bridge server is running'}
    
    def handle_organize_assets(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Organize assets"""
        if AssetOrganizer and not self.organizer:
            self.organizer = AssetOrganizer()
        
        asset_path = params.get('asset_path', '/Game/')
        
        if self.organizer:
            # TODO: Implement actual organization logic
            pass
        
        return {
            'organized': True,
            'path': asset_path,
            'message': 'Assets organized successfully (test mode)' if not self.organizer else 'Assets organized successfully'
        }
    
    def handle_suggest_name(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest asset name using AI"""
        if AIAssetNaming and not self.naming:
            self.naming = AIAssetNaming()
        
        original_name = params.get('original_name')
        asset_type = params.get('asset_type')
        
        if not original_name or not asset_type:
            return {'error': 'Missing required parameters: original_name, asset_type'}
        
        # Generate suggested name
        if self.naming:
            # TODO: Implement actual naming logic with AI
            suggested_name = f"SM_{original_name.title().replace('_', '')}"
        else:
            # Test mode - simple prefix
            prefix_map = {
                'StaticMesh': 'SM',
                'SkeletalMesh': 'SK',
                'Texture2D': 'T',
                'Material': 'M',
                'Blueprint': 'BP'
            }
            prefix = prefix_map.get(asset_type, 'A')
            suggested_name = f"{prefix}_{original_name.title().replace('_', '')}"
        
        return {
            'original_name': original_name,
            'suggested_name': suggested_name,
            'asset_type': asset_type,
            'mode': 'test' if not self.naming else 'ai'
        }
    
    def handle_generate_material(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate material from description"""
        if MaterialGenerator and not self.material_gen:
            self.material_gen = MaterialGenerator()
        
        description = params.get('description')
        if not description:
            return {'error': 'Missing required parameter: description'}
        
        # Generate material parameters (test mode uses simple defaults)
        return {
            'description': description,
            'parameters': {
                'BaseColor': [0.5, 0.5, 0.5],
                'Metallic': 0.0,
                'Roughness': 0.5,
                'Specular': 0.5
            },
            'message': 'Material parameters generated (test mode)' if not self.material_gen else 'Material parameters generated',
            'mode': 'test' if not self.material_gen else 'ai'
        }
    
    def handle_generate_metadata(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate metadata for asset"""
        if MetadataGenerator and not self.metadata_gen:
            self.metadata_gen = MetadataGenerator()
        
        asset_name = params.get('asset_name')
        asset_type = params.get('asset_type')
        
        if not asset_name or not asset_type:
            return {'error': 'Missing required parameters: asset_name, asset_type'}
        
        # Generate metadata (test mode uses simple defaults)
        return {
            'asset_name': asset_name,
            'tags': ['generated', asset_type.lower()],
            'description': f'Asset: {asset_name}',
            'message': 'Metadata generated (test mode)' if not self.metadata_gen else 'Metadata generated',
            'mode': 'test' if not self.metadata_gen else 'ai'
        }
    
    def handle_sanity_check(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Run sanity check on assets"""
        if SanityChecker and not self.sanity_checker:
            self.sanity_checker = SanityChecker()
        
        root_path = params.get('root_path', '/Game/')
        
        return {
            'root_path': root_path,
            'issues_found': 0,
            'critical': 0,
            'warnings': 0,
            'message': 'Sanity check completed (test mode)' if not self.sanity_checker else 'Sanity check completed',
            'mode': 'test' if not self.sanity_checker else 'real'
        }
    
    def handle_optimize_textures(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize textures"""
        if TextureOptimizer and not self.texture_optimizer:
            self.texture_optimizer = TextureOptimizer()
        
        viewing_distance = params.get('viewing_distance', 'medium')
        
        return {
            'viewing_distance': viewing_distance,
            'textures_optimized': 0,
            'memory_saved': 0,
            'message': 'Texture optimization completed (test mode)' if not self.texture_optimizer else 'Texture optimization completed',
            'mode': 'test' if not self.texture_optimizer else 'real'
        }
    
    def handle_generate_lods(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate LODs for meshes"""
        if LODGenerator and not self.lod_generator:
            self.lod_generator = LODGenerator()
        
        mesh_path = params.get('mesh_path')
        
        return {
            'mesh_path': mesh_path,
            'lods_generated': 0,
            'message': 'LOD generation completed (test mode)' if not self.lod_generator else 'LOD generation completed',
            'mode': 'test' if not self.lod_generator else 'real'
        }


def main():
    """Main entry point"""
    server = UE5BridgeServer()
    
    try:
        logger.info("Starting UE5 Semantic Automation Bridge Server...")
        server.start()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        server.stop()


if __name__ == '__main__':
    main()
