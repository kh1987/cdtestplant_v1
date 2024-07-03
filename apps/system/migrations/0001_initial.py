# Generated by Django 4.2.13 on 2024-07-03 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OperationLog',
            fields=[
                ('id', models.BigAutoField(help_text='Id', primary_key=True, serialize=False, verbose_name='Id')),
                ('remark', models.CharField(blank=True, help_text='描述', max_length=255, null=True, verbose_name='描述')),
                ('modifier', models.CharField(blank=True, help_text='修改人', max_length=255, null=True, verbose_name='修改人')),
                ('request_username', models.CharField(blank=True, help_text='请求用户', max_length=50, null=True, verbose_name='请求用户')),
                ('request_modular', models.CharField(blank=True, help_text='请求模块', max_length=64, null=True, verbose_name='请求模块')),
                ('request_path', models.CharField(blank=True, help_text='请求地址', max_length=400, null=True, verbose_name='请求地址')),
                ('request_body', models.TextField(blank=True, help_text='请求参数', null=True, verbose_name='请求参数')),
                ('request_method', models.CharField(blank=True, help_text='请求方式', max_length=8, null=True, verbose_name='请求方式')),
                ('request_msg', models.TextField(blank=True, help_text='操作说明', null=True, verbose_name='操作说明')),
                ('request_ip', models.CharField(blank=True, help_text='请求ip地址', max_length=32, null=True, verbose_name='请求ip地址')),
                ('request_browser', models.CharField(blank=True, help_text='请求浏览器', max_length=64, null=True, verbose_name='请求浏览器')),
                ('response_code', models.CharField(blank=True, help_text='响应状态码', max_length=32, null=True, verbose_name='响应状态码')),
                ('request_os', models.CharField(blank=True, help_text='操作系统', max_length=64, null=True, verbose_name='操作系统')),
                ('json_result', models.TextField(blank=True, help_text='返回信息', null=True, verbose_name='返回信息')),
                ('status', models.BooleanField(default=False, help_text='响应状态', verbose_name='响应状态')),
                ('update_datetime', models.DateTimeField(auto_now=True, help_text='修改时间', null=True, verbose_name='修改时间')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True, verbose_name='创建时间')),
                ('sort', models.IntegerField(blank=True, default=1, help_text='显示排序', null=True, verbose_name='显示排序')),
                ('creator', models.ForeignKey(db_constraint=False, help_text='创建人', null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
            ],
            options={
                'verbose_name': '操作日志',
                'verbose_name_plural': '操作日志',
                'db_table': 'system_operation_log',
                'ordering': ('-create_datetime',),
            },
        ),
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('id', models.BigAutoField(help_text='Id', primary_key=True, serialize=False, verbose_name='Id')),
                ('remark', models.CharField(blank=True, help_text='描述', max_length=255, null=True, verbose_name='描述')),
                ('modifier', models.CharField(blank=True, help_text='修改人', max_length=255, null=True, verbose_name='修改人')),
                ('username', models.CharField(blank=True, help_text='登录用户名', max_length=32, null=True, verbose_name='登录用户名')),
                ('ip', models.CharField(blank=True, help_text='登录ip', max_length=32, null=True, verbose_name='登录ip')),
                ('agent', models.TextField(blank=True, help_text='agent信息', null=True, verbose_name='agent信息')),
                ('browser', models.CharField(blank=True, help_text='浏览器名', max_length=200, null=True, verbose_name='浏览器名')),
                ('os', models.CharField(blank=True, help_text='操作系统', max_length=200, null=True, verbose_name='操作系统')),
                ('country', models.CharField(blank=True, help_text='国家', max_length=50, null=True, verbose_name='国家')),
                ('login_type', models.IntegerField(choices=[(1, '普通登录')], default=1, help_text='登录类型', verbose_name='登录类型')),
                ('update_datetime', models.DateTimeField(auto_now=True, help_text='修改时间', null=True, verbose_name='修改时间')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True, verbose_name='创建时间')),
                ('sort', models.IntegerField(blank=True, default=1, help_text='显示排序', null=True, verbose_name='显示排序')),
                ('creator', models.ForeignKey(db_constraint=False, help_text='创建人', null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
            ],
            options={
                'verbose_name': '登录日志',
                'verbose_name_plural': '登录日志',
                'db_table': 'system_login_log',
                'ordering': ('-create_datetime',),
            },
        ),
    ]
