@echo off
echo Creating virtual environment...
python -m venv .venv

echo Installing dependencies...
call .venv\Scripts\activate.bat
pip install -r requirements.txt

echo Setup complete!
echo To start the app, run:
echo .venv\Scripts\activate.bat
echo python main.py
pause
