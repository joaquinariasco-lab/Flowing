#!/bin/bash

echo "🚀 Installing Flowing..."

# Create virtual env
python3 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

echo "✅ Installation complete."
echo ""
echo "Run the demo with:"
echo "./run.sh"
