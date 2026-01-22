@echo off
:: 1. Entramos a la nueva carpeta de AUTOMATIZACION
cd /d "C:\Users\gutyp\Desktop\Naranja\AUTOMATIZACION"

:: 2. Ejecutamos el script (Asegurate de que el archivo .py esté en esta misma carpeta)
python incident_response.py

:: 3. Creamos un registro para saber que el robot trabajó
echo Patrullaje ejecutado con exito el %date% a las %time% >> log_historico.txt

:: Mantenemos la ventana abierta un segundo para ver si hay errores (luego lo podés quitar)
timeout /t 10