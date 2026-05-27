@echo off
cd /d "%~dp0"
echo Installing dependencies...
py -m pip install -r requirements.txt
echo.
echo Starting dashboard...
py -m streamlit run welcome_gui.py
pause