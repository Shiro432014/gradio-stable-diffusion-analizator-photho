@echo off
REM Всегда запускаем из папки, где лежит батник
cd /d "%~dp0"

REM Активируем виртуальное окружение
call venv\Scripts\activate

REM Запускаем приложение прямо в этом окне
python app.py

REM Оставляем окно открытым для логов
pause
