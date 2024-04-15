@echo off

echo ��ʹ�ù���Ա���иýű�

echo �������û�������...
set currentDir=%~dp0
set currentDir=%currentDir%\mysql-8.0.36-winx64
set basedir=%currentDir%

echo **********��ǰmysql��·��:%basedir%**********

setx /M PATH "%basedir%bin;%path%"

echo **********��ʼ�����ݿ������ļ�**********
echo **********ɾ��init�����ļ�**********

del %basedir%\my.ini

echo **********����init�����ļ���ע��˿ں�Ϊ3307������Ϊ��ĳЩ��װ��mysql�Ľ��лر�**********

@echo [mysqld]>>%basedir%\my.ini
@echo port=3307>>%basedir%\my.ini
@echo basedir=%basedir%>>%basedir%\my.ini
@echo datadir=%basedir%\data>>%basedir%\my.ini
@echo max_connections=200>>%basedir%\my.ini
@echo max_connect_errors=10>>%basedir%\my.ini
@echo character-set-server=utf8mb4>>%basedir%\my.ini
@echo default-storage-engine=INNODB>>%basedir%\my.ini
@echo default_authentication_plugin=mysql_native_password>>%basedir%\my.ini
@echo [mysql]>>%basedir%\my.ini
@echo default-character-set=utf8mb4>>%basedir%\my.ini
@echo [client]>>%basedir%\my.ini
@echo default-character-set=utf8mb4>>%basedir%\my.ini
@echo port=3307>>%basedir%\my.ini

echo **********��ʼ�����ݿ���**********
%basedir%\bin\mysqld.exe --initialize-insecure --lower-case-table-names=1 --user=mysql --console

echo **********��ʼ��װ���ݿ�**********
%basedir%\bin\mysqld.exe --install mysql80

echo **********��װ���񣬺������80���ͱ���mysql�����ͻ**********
net start mysql80