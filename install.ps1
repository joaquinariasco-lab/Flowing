Write-Host "🚀 Installing Flowing..."

# Create virtual environment
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..."
& .\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

Write-Host "✅ Installation complete. Starting demo..."

# Run the demo automatically
.\run.ps1
