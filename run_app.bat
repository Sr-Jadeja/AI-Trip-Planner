@echo off
cd /d "%~dp0"

start "FastAPI Backend" cmd /k "uvicorn main:app --reload"

timeout /t 3 /noisy >nul

start "Streamlit Frontend" cmd /k "streamlit run streamlit_app.py"