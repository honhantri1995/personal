@echo off

echo -------------------------
taskkill /t /f /im chromedriver.exe
echo Killed chromedriver.exe

echo.
echo -------------------------
taskkill /t /f /im python.exe
echo Killed python.exe

pause