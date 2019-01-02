# Generated by Django 2.1.4 on 2018-12-26 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AtionLogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updateTime', models.DateTimeField(auto_now=True)),
                ('ationlog', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BaseFuntion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('functionname', models.CharField(max_length=30, unique=True)),
                ('functionURL', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500, null=True)),
                ('remarks', models.CharField(max_length=500, null=True)),
                ('isnewview', models.CharField(max_length=15, null=True)),
                ('isenable', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='FuntionRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('function', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MySite.BaseFuntion')),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=50, unique=True)),
                ('ip', models.CharField(max_length=50)),
                ('remarks', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ParentProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectname', models.CharField(max_length=50, unique=True)),
                ('remarks', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectForHost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MySite.Host')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rolename', models.CharField(max_length=30, unique=True)),
                ('remarks', models.CharField(max_length=500, null=True)),
                ('isenable', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Subproject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectname', models.CharField(max_length=50, unique=True)),
                ('projectaddress', models.CharField(max_length=100)),
                ('remarks', models.CharField(max_length=500, null=True)),
                ('ParentProject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MySite.ParentProject')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('staffname', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=30, null=True)),
                ('isenable', models.IntegerField(default=1)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MySite.Role')),
            ],
        ),
        migrations.CreateModel(
            name='VersionList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=100, null=True)),
                ('updateTime', models.DateTimeField(auto_now=True)),
                ('ation', models.CharField(max_length=30)),
                ('remarks', models.CharField(max_length=50, null=True)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MySite.Host')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MySite.Subproject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MySite.UserInfo')),
            ],
        ),
        migrations.AddField(
            model_name='projectforhost',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MySite.Subproject'),
        ),
        migrations.AddField(
            model_name='funtionrole',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MySite.Role'),
        ),
        migrations.AddField(
            model_name='ationlogs',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MySite.UserInfo'),
        ),
    ]