@echo off
REM ============================================================
REM MyClassboard Games - Automatic PostgreSQL Setup
REM ============================================================

echo.
echo ============================================================
echo MyClassboard Games - PostgreSQL Setup
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Check if psycopg2 is installed
python -c "import psycopg2" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing psycopg2 (PostgreSQL driver for Python)...
    pip install psycopg2-binary
)

REM Run setup script
echo.
echo Starting automatic setup...
echo.
python setup_database.py

if errorlevel 1 (
    echo.
    echo ERROR: Setup failed!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Press any key to close this window
echo   2. Run: python app.py
echo   3. Test: curl http://localhost:5000/api/curriculum
echo.
pause
