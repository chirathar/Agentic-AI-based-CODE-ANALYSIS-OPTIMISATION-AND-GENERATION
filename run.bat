@echo off
REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install dependencies
pip install -r env/requirements.txt

REM Start Flask server
echo.
echo ========================================
echo Starting Python Code Analyzer...
echo ========================================
echo.
echo Open your browser and go to: http://localhost:5000
echo.
python app.py

pause
