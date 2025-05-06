@echo off
echo ================================
echo AVVIO GESTIONALE + TUNNEL CLOUDFLARE
echo ================================
REM Avvia il gestionale API in background
start cmd /k "python app_api.py"

REM Attendere qualche secondo per avvio server
timeout /t 5

REM Avvia il tunnel (modifica il nome con il tuo se già configurato)
echo Avvio del tunnel...
cloudflared tunnel run gestionale-cani
