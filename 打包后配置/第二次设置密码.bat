echo off
echo ��ʼ������...

set currentDir=%~dp0
set currentDirBase=%currentDir%\mysql-8.0.36-winx64
set basedir=%currentDirBase%

echo ��ǰ·��Ϊ%basedir%

@%basedir%\bin\mysql.exe -uroot -proot < %currentDir%\setpwd.sql
echo ��ʼ��������ϣ��û���Ϊ��root��������Ϊ��root�����������
pause