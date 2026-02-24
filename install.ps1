Write-Host "🚀 Installing Flowing..."

python -m venv venv
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt

Write-Host "✅ Installation complete."
Write-Host ""
Write-Host "Run the demo with:"
Write-Host ".\run.ps1"
