use mysql;
select Host, User from user;
update user set authentication_string='' where user='root';
update user set host='%' where user='root';
flush privileges;
alter user 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'root';
flush privileges;
CREATE DATABASE chengdu_test_plant_v1 CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
exit