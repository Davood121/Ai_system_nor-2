@echo off
set PATH=%PATH%;C:\Program Files\Git\bin
cd /d "c:\Users\shaik\Desktop\Ai"
git --version
git init
git remote add origin https://github.com/Davood121/Ai_system_nor.git
git add .
git commit -m "Complete AI Assistant System with consciousness and stories"
git branch -M main
git push -u origin main
pause