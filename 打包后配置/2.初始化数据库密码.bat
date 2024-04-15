echo off
echo 初始化密码...

set currentDir=%~dp0
set currentDirBase=%currentDir%\mysql-8.0.36-winx64
set basedir=%currentDirBase%

echo 当前路径为%basedir%

@%basedir%\bin\mysql.exe -uroot < %currentDir%\setpwd.sql

echo 初始化密码完毕，用户名为“root”，密码为“root”，请勿更改

echo ~~~~~~~~~~正在初始化项目数据库~~~~~~~~~~
@%basedir%\bin\mysql.exe -uroot -proot -D chengdu_test_plant_v1 --default-character-set=utf8 < dbdata.sql
echo ~~~~~~~~~~初始化项目数据库结束~~~~~~~~~~

pause
