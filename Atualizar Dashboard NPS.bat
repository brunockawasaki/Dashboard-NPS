@echo off
chcp 65001 >nul
cd /d "%~dp0"
python gerar_dashboard_nps.py
if errorlevel 1 (
  echo.
  echo Algo deu errado. Veja a mensagem acima.
  pause
  exit /b 1
)
echo.
echo Pronto. Abra o arquivo "Dashboard NPS.html" na pasta NPS e aperte F5 se ele ja estiver aberto.
pause
