@echo off
echo ============================================
echo   Marketing Hub — Setup Script
echo ============================================
echo.

echo [1/3] Installing Python packages...
pip install -r requirements.txt
echo Done.
echo.

echo [2/3] Checking for .env file...
IF NOT EXIST ".env" (
    copy .env.example .env
    echo Created .env file — OPEN IT and paste your Anthropic API key!
    echo File location: %CD%\.env
) ELSE (
    echo .env file already exists. Good.
)
echo.

echo [3/3] Setup complete!
echo.
echo To START the app, run:   start.bat
echo Or type:                 python -m streamlit run app.py
echo.
pause
