@echo off
REM Python Code Analyzer & Optimizer - Frontend Startup

echo.
echo ==========================================
echo Python Code Analyzer ^& Optimizer
echo ==========================================
echo.

REM Check if venv exists
if not exist ".venv" (
    echo Error: Virtual environment not found!
    echo Please run: python -m venv .venv
    pause
    exit /b 1
)

REM Activate venv
echo [1/3] Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo [2/3] Checking dependencies...
pip install -q -r env/requirements.txt

REM Start Flask server
echo [3/3] Starting Flask server...
echo.
echo OK - Frontend is running at: http://localhost:5000
echo.
echo For optimization features, ensure Ollama is running:
echo   ollama serve
echo.
echo Press CTRL+C to stop the server
echo.

python app.py
pause
