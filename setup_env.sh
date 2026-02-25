#!/bin/bash
# Bash script to set up environment variables for UE5 Semantic Automation

echo "=== UE5 Semantic Automation - Environment Setup ==="
echo ""

# Detect shell config file
if [ -f "$HOME/.zshrc" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
elif [ -f "$HOME/.bash_profile" ]; then
    SHELL_CONFIG="$HOME/.bash_profile"
else
    SHELL_CONFIG="$HOME/.profile"
fi

echo "Shell config file: $SHELL_CONFIG"
echo ""

# Check if API key is already set
if grep -q "OPENAI_API_KEY" "$SHELL_CONFIG"; then
    echo "⚠️  OPENAI_API_KEY is already configured in $SHELL_CONFIG"
    echo ""
    read -p "Do you want to update it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Keeping existing API key."
        exit 0
    fi
    # Remove old entry
    sed -i.bak '/OPENAI_API_KEY/d' "$SHELL_CONFIG"
fi

echo "Please enter your API key:"
read -s API_KEY

if [ -z "$API_KEY" ]; then
    echo "✗ No API key provided. Exiting."
    exit 1
fi

# Add to shell config
echo "" >> "$SHELL_CONFIG"
echo "# UE5 Semantic Automation API Key" >> "$SHELL_CONFIG"
echo "export OPENAI_API_KEY=\"$API_KEY\"" >> "$SHELL_CONFIG"

echo ""
echo "✓ Environment variable added to $SHELL_CONFIG"
echo ""
echo "IMPORTANT: Run the following command to apply changes:"
echo "  source $SHELL_CONFIG"
echo ""
echo "Or restart your terminal."
echo ""
echo "To verify, run: echo \$OPENAI_API_KEY"
echo ""
echo "Setup complete! 🎉"
