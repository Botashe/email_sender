@echo off
REM Activar entorno virtual
call venv_email_sender_app\Scripts\activate.bat

REM Ejecutar PyInstaller para crear el ejecutable
py -m PyInstaller --name email_sender_app --onefile --windowed --icon=email_sender_app/assets/icon.ico --add-data "email_sender_app/assets;assets" --hidden-import pymysql --hidden-import bcrypt email_sender_app/app.py

REM Pausa para ver resultados
pause
