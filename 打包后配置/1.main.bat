@echo off
echo ~~~~~~~~~~开始安装mysql，并启动服务~~~~~~~~~~
call my_install.bat
echo ~~~~~~~~~~安装mysql完毕已启动服务~~~~~~~~~~

echo ~~~~~~~~~~开始安装nginx~~~~~~~~~~
call nginx_start.bat
echo ~~~~~~~~~~nginx服务已启动~~~~~~~~~~

echo !!!!!!!!!!!!!请执行2.初始化数据库密码批处理!!!!!!!!!!!!!

pause