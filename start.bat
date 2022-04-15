@echo off
ECHO "Quante generazioni vuoi fare?"
FOR /F "tokens=*" %%A IN ('TYPE CON') DO SET INPUT=%%A
ECHO "Okiei"
SET TIMES=0
:B
C:/Users/Matte/AppData/Local/Programs/Python/Python310/python.exe main.py 
SET /A TIMES=%TIMES%+1
ECHO %TIMES%
IF %TIMES% LSS %INPUT% goto :B

