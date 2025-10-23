@echo off
echo Uploading AI System to GitHub...
echo.

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo Git is not installed. Please install Git first:
    echo https://git-scm.com/download/win
    pause
    exit /b 1
)

REM Initialize repository
echo Initializing Git repository...
git init

REM Add remote repository
echo Adding remote repository...
git remote add origin https://github.com/Davood121/Ai_system_nor.git

REM Add all files
echo Adding files...
git add .

REM Commit changes
echo Committing changes...
git commit -m "Initial commit: Complete AI Assistant System with consciousness, stories, and multi-language support"

REM Push to GitHub
echo Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo Upload complete! Your AI system is now on GitHub.
echo Repository: https://github.com/Davood121/Ai_system_nor.git
pause