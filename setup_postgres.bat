@echo off
REM PostgreSQL Setup Script for Windows
REM This script helps set up PostgreSQL for MyClassboard Games

echo.
echo ========================================================
echo PostgreSQL Setup for MyClassboard Games
echo ========================================================
echo.

echo Please ensure PostgreSQL is installed and running.
echo If not, download from: https://www.postgresql.org/download/windows/
echo.

echo Step 1: Update .env file
echo ========================
echo Edit the .env file with your PostgreSQL credentials:
echo   DATABASE_URL=postgresql://myclassboard_user:your_password@localhost:5432/myclassboard_games
echo.
pause

echo Step 2: Create Database and User
echo ==================================
echo Run these commands in PostgreSQL command line (psql):
echo.
echo   psql -U postgres
echo.
echo Then paste these SQL commands:
echo.
echo   CREATE DATABASE myclassboard_games;
echo   CREATE USER myclassboard_user WITH PASSWORD 'your_secure_password';
echo   ALTER ROLE myclassboard_user SET client_encoding TO 'utf8';
echo   ALTER ROLE myclassboard_user SET default_transaction_isolation TO 'read committed';
echo   ALTER ROLE myclassboard_user SET default_transaction_deferrable TO on;
echo   ALTER ROLE myclassboard_user SET default_time_zone TO 'UTC';
echo   GRANT ALL PRIVILEGES ON DATABASE myclassboard_games TO myclassboard_user;
echo   \c myclassboard_games
echo   GRANT ALL ON SCHEMA public TO myclassboard_user;
echo   \q
echo.
pause

echo Step 3: Install Python Dependencies
echo =====================================
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Error installing dependencies!
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo Step 4: Initialize Database
echo ============================
python app.py
echo.
echo If you see "Database: PostgreSQL ✅" the setup is successful!
echo.
pause
