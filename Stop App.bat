@echo off
title Stop TN Transport AI
echo Stopping background app server...
taskkill /F /IM pythonw.exe >nul 2>&1
echo.
echo ==========================================================
echo   TN Smart Transport AI App stopped successfully.
echo ==========================================================
echo.
pause
