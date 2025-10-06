@echo off
REM BOB Google Maps V3.0.1 - Automated Setup Script
REM Author: Divyanshu Singh Chouhan
REM Platform: Windows

echo ============================================
echo BOB Google Maps V3.0.1 - Automated Setup
echo ============================================
echo.

echo Detected OS: Windows
echo.

REM Check Python
echo Checking Python version...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Please install Python 3.10+
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo Python %PYTHON_VERSION% found
echo.

echo Installing BOB package...
python -m pip install -e . --quiet
if %errorlevel% neq 0 (
    echo Installation failed
    pause
    exit /b 1
)

echo.
echo Installing Playwright browsers...
python -m playwright install chromium --quiet
if %errorlevel% neq 0 (
    echo Playwright installation failed
    pause
    exit /b 1
)

echo.
echo Verifying installation...
python -c "from bob_v3 import __version__; print(f'BOB v{__version__} installed successfully')"

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo Quick Start:
echo   Single extraction:    python -m bob_v3 "Business Name"
echo   Batch extraction:     python -m bob_v3 --batch urls.txt --parallel
echo   Docker deployment:    docker compose up -d
echo.
echo Documentation: README.md
echo Jai Shree Krishna!
echo.
pause
