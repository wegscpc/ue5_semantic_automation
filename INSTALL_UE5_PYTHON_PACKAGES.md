# Installing Python Packages for UE5's Python Environment

Unreal Engine 5 uses its own embedded Python installation, separate from your system Python. To use AI features, you need to install packages in UE5's Python environment.

## Method 1: Using UE5's Python Console (Recommended)

1. **Open UE5 Python Console**
   - Window → Developer Tools → Output Log
   - Select "Python" from dropdown

2. **Install packages directly in UE5**:

```python
import subprocess
import sys

# Get UE5's Python executable path
python_exe = sys.executable
print(f"UE5 Python: {python_exe}")

# Install anthropic
subprocess.check_call([python_exe, "-m", "pip", "install", "anthropic"])

print("✓ Anthropic installed successfully!")
```

## Method 2: Find UE5's Python and Install Manually

1. **Find UE5's Python executable** - Run this in UE5 Python console:

```python
import sys
print(f"Python executable: {sys.executable}")
```

2. **Install packages using that Python**:

Open PowerShell and run:
```powershell
# Replace with your actual UE5 Python path
& "C:\Program Files\Epic Games\UE_5.X\Engine\Binaries\ThirdParty\Python3\Win64\python.exe" -m pip install anthropic
```

Common UE5 Python locations:
- **UE 5.0-5.4**: `C:\Program Files\Epic Games\UE_5.X\Engine\Binaries\ThirdParty\Python3\Win64\python.exe`
- **Custom Install**: Check your UE5 installation directory

## Method 3: Install All Required Packages

Run this in UE5 Python console to install all dependencies:

```python
import subprocess
import sys

packages = [
    "anthropic>=0.18.0",
    "openai>=1.0.0",
    "requests>=2.28.0"
]

python_exe = sys.executable

for package in packages:
    print(f"Installing {package}...")
    try:
        subprocess.check_call([python_exe, "-m", "pip", "install", package])
        print(f"✓ {package} installed")
    except Exception as e:
        print(f"✗ Failed to install {package}: {e}")

print("\n✓ All packages installed!")
```

## Verify Installation

After installation, verify in UE5 Python console:

```python
# Test anthropic
try:
    import anthropic
    print(f"✓ Anthropic version: {anthropic.__version__}")
except ImportError:
    print("✗ Anthropic not installed")

# Test openai
try:
    import openai
    print(f"✓ OpenAI version: {openai.__version__}")
except ImportError:
    print("✗ OpenAI not installed")
```

## Troubleshooting

### "No module named pip"

If pip is not available in UE5's Python:

```python
import subprocess
import sys

# Download get-pip.py
import urllib.request
url = "https://bootstrap.pypa.io/get-pip.py"
urllib.request.urlretrieve(url, "get-pip.py")

# Install pip
subprocess.check_call([sys.executable, "get-pip.py"])

print("✓ pip installed!")
```

### Permission Denied

Run Unreal Engine as Administrator, then try installing packages again.

### Package Not Found

Ensure you have internet connection and try:
```python
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
```

## After Installation

Once packages are installed, restart Unreal Engine and test the AI features:

```python
import sys
# Replace with your actual project path
sys.path.append('/path/to/your/ue5_semantic_automation/src')

from ai.llm_client import LLMClient, LLMProvider
import unreal

client = LLMClient(provider=LLMProvider.ANTHROPIC)
print("✓ Claude client initialized successfully!")
```
