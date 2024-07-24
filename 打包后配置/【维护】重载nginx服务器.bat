@ECHO off
set currentDir=%~dp0
set currentDirBase=%currentDir%\nginx-1.24.0
set basedir=%currentDirBase%

cd %basedir%
.\nginx -s reload