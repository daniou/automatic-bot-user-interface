@echo off
setlocal

:: Especifica la versión de Python a descargar
set PYTHON_VERSION=3.10.0

:: Define la URL del instalador de Python
set PYTHON_INSTALLER_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe

:: Define el nombre del archivo del instalador
set PYTHON_INSTALLER_FILE=python-installer.exe

:: Descarga el instalador de Python
echo Descargando Python %PYTHON_VERSION%...
powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri %PYTHON_INSTALLER_URL% -OutFile %PYTHON_INSTALLER_FILE%"

:: Verifica si el archivo se descargó correctamente
if not exist %PYTHON_INSTALLER_FILE% (
    echo Error: No se pudo descargar el instalador de Python.
    exit /b 1
)

:: Instala Python
echo Instalando Python %PYTHON_VERSION%...
start /wait %PYTHON_INSTALLER_FILE% /quiet InstallAllUsers=1 PrependPath=1

:: Agrega Python al PATH del sistema
setx PATH "%PATH%;C:\Python%PYTHON_VERSION%\;C:\Python%PYTHON_VERSION%\Scripts\"

:: Verifica si Python se instaló correctamente
if errorlevel 1 (
    echo Error: La instalación de Python falló.
    exit /b 1
)

echo Python %PYTHON_VERSION% instalado correctamente.

:: Limpieza del instalador
del %PYTHON_INSTALLER_FILE%

:: Fin del script
endlocal
