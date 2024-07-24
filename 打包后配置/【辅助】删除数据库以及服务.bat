@ECHO off
@echo 重新初始化

set currentDir=%~dp0

set currentDirBase=%currentDir%mysql-8.0.36-winx64
set basedir=%currentDirBase%

set binpath=%basedir%\bin
set myinipath=%basedir%\my.ini
set datapath=%basedir%\data

net stop mysql80
cd %binpath%
%basedir%\bin\mysqld.exe --remove mysql80
rmdir /s/q %datapath%
del %myinipath%

pause