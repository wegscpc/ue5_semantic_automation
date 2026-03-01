"""
Build Script for UE5 Semantic Automation Plugin

This script automates the building and packaging of the plugin for Unreal Engine 5.
Based on the Convai-UnrealEngine-SDK build pattern.

Usage:
    python Build.py [Unreal Engine Directory] [Additional Flags]
    
Example:
    python Build.py "C:\\Program Files\\Epic Games\\UE_5.3" -TargetPlatforms=Win64
"""

import os
import sys
import subprocess
import shutil
import argparse
from pathlib import Path


class PluginBuilder:
    def __init__(self, ue_path: str, target_platforms: str = "Win64"):
        self.ue_path = Path(ue_path)
        self.target_platforms = target_platforms
        self.plugin_root = Path(__file__).parent
        self.plugin_name = "UE5SemanticAutomation"
        self.output_dir = self.plugin_root / "Output"
        
        # Validate UE path
        if not self.ue_path.exists():
            raise ValueError(f"Unreal Engine path does not exist: {self.ue_path}")
        
        # Find UAT
        self.uat_path = self.find_uat()
        if not self.uat_path:
            raise ValueError("Could not find UnrealAutomationTool (UAT)")
    
    def find_uat(self) -> Path:
        """Find UnrealAutomationTool executable"""
        # Windows
        uat_bat = self.ue_path / "Engine" / "Build" / "BatchFiles" / "RunUAT.bat"
        if uat_bat.exists():
            return uat_bat
        
        # Mac/Linux
        uat_sh = self.ue_path / "Engine" / "Build" / "BatchFiles" / "RunUAT.sh"
        if uat_sh.exists():
            return uat_sh
        
        return None
    
    def clean_output(self):
        """Clean output directory"""
        if self.output_dir.exists():
            print(f"Cleaning output directory: {self.output_dir}")
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def build_plugin(self):
        """Build the plugin using UAT"""
        print(f"\n{'='*60}")
        print(f"Building {self.plugin_name} Plugin")
        print(f"{'='*60}\n")
        
        uplugin_path = self.plugin_root / f"{self.plugin_name}.uplugin"
        
        if not uplugin_path.exists():
            raise ValueError(f"Plugin descriptor not found: {uplugin_path}")
        
        # Build command
        cmd = [
            str(self.uat_path),
            "BuildPlugin",
            f"-Plugin={uplugin_path}",
            f"-Package={self.output_dir}",
            f"-TargetPlatforms={self.target_platforms}",
            "-Rocket"  # For binary engine builds
        ]
        
        print(f"Running command: {' '.join(cmd)}\n")
        
        # Execute build
        result = subprocess.run(cmd, cwd=str(self.plugin_root))
        
        if result.returncode != 0:
            raise RuntimeError(f"Build failed with exit code {result.returncode}")
        
        print(f"\n{'='*60}")
        print(f"Build completed successfully!")
        print(f"Output: {self.output_dir}")
        print(f"{'='*60}\n")
    
    def copy_python_files(self):
        """Copy Python files to output"""
        print("Copying Python files...")
        
        python_src = self.plugin_root / "Python"
        python_dst = self.output_dir / self.plugin_name / "Python"
        
        if python_src.exists():
            shutil.copytree(python_src, python_dst, dirs_exist_ok=True)
            print(f"Python files copied to {python_dst}")
    
    def create_readme(self):
        """Create README in output directory"""
        readme_content = f"""# {self.plugin_name} - Build Output

This directory contains the compiled plugin ready for installation.

## Installation

### Method 1: Engine Plugins Directory (Recommended)
Copy the entire `{self.plugin_name}` folder to:
- Windows: `C:\\Program Files\\Epic Games\\UE_5.x\\Engine\\Plugins\\Marketplace\\`
- Mac: `/Users/Shared/Epic Games/UE_5.x/Engine/Plugins/Marketplace/`
- Linux: `~/UnrealEngine/UE_5.x/Engine/Plugins/Marketplace/`

### Method 2: Project Plugins Directory
Copy the entire `{self.plugin_name}` folder to:
`YourProject/Plugins/{self.plugin_name}/`

## Starting the Python Bridge

Before using the plugin, start the Python bridge server:

```bash
cd {self.plugin_name}/Python
python bridge_server.py
```

The bridge server will listen on port 55557 for connections from the UE5 plugin.

## Verification

1. Open Unreal Engine
2. Go to Edit → Plugins
3. Search for "{self.plugin_name}"
4. Enable the plugin
5. Restart Unreal Engine
6. Look for the "Semantic Automation" button in the toolbar

## Documentation

See the main project repository for full documentation:
https://github.com/wegscpc/ue5_semantic_automation
"""
        
        readme_path = self.output_dir / "README.md"
        readme_path.write_text(readme_content)
        print(f"README created: {readme_path}")


def main():
    parser = argparse.ArgumentParser(description='Build UE5 Semantic Automation Plugin')
    parser.add_argument('ue_path', help='Path to Unreal Engine installation')
    parser.add_argument('-TargetPlatforms', default='Win64', 
                       help='Target platforms (default: Win64)')
    
    args = parser.parse_args()
    
    try:
        builder = PluginBuilder(args.ue_path, args.TargetPlatforms)
        
        # Build steps
        builder.clean_output()
        builder.build_plugin()
        builder.copy_python_files()
        builder.create_readme()
        
        print("\n✅ Plugin build completed successfully!")
        print(f"📦 Output location: {builder.output_dir}")
        print("\n📖 See Output/README.md for installation instructions")
        
    except Exception as e:
        print(f"\n❌ Build failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
