echo off
echo ��ʼ������...

set currentDir=%~dp0
set currentDirBase=%currentDir%\mysql-8.0.36-winx64
set basedir=%currentDirBase%

echo ��ǰ·��Ϊ%basedir%

@%basedir%\bin\mysql.exe -uroot < %currentDir%\setpwd.sql

echo ��ʼ��������ϣ��û���Ϊ��root��������Ϊ��root�����������

echo ~~~~~~~~~~���ڳ�ʼ����Ŀ���ݿ�~~~~~~~~~~
@%basedir%\bin\mysql.exe -uroot -proot -D chengdu_test_plant_v1 --default-character-set=utf8 < dbdata.sql
echo ~~~~~~~~~~��ʼ����Ŀ���ݿ����~~~~~~~~~~

pause
