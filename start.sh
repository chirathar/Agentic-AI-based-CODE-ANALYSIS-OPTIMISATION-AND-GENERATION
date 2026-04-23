#!/bin/bash
# Quick startup script for the frontend

echo "=========================================="
echo "Python Code Analyzer & Optimizer"
echo "=========================================="
echo ""

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run: python -m venv .venv"
    exit 1
fi

# Activate venv
echo "[1/3] Activating virtual environment..."
source .venv/Scripts/activate

# Install dependencies if needed
echo "[2/3] Checking dependencies..."
pip install -q -r env/requirements.txt

# Start Flask server
echo "[3/3] Starting Flask server..."
echo ""
echo "✓ Frontend running at: http://localhost:5000"
echo "✓ Press CTRL+C to stop"
echo ""
echo "For optimization features, ensure Ollama is running:"
echo "  ollama serve"
echo ""

python app.py
