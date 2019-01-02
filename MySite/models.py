from django.db import models

#角色表
class Role(models.Model):
    rolename = models.CharField(unique=True, max_length=30)                 #角色名字
    remarks = models.CharField(null=True, max_length=500)                   #角色说明
    isenable = models.IntegerField(default=1)                               #是否启用

#权限功能表
class BaseFuntion(models.Model):
    functionname = models.CharField(unique=True,max_length=30)              #功能名称
    functionURL = models.CharField(max_length=100)                          #功能链接
    description = models.CharField(null=True, max_length=500)               #功能作用
    remarks = models.CharField(null=True, max_length=500)                   #功能说明
    isnewview   = models.CharField(null=True,max_length=15)                 #是否在新窗口打开
    isenable = models.IntegerField(default=1)                               #是否启用

#角色权限对应表
class FuntionRole(models.Model):
    role = models.ForeignKey('Role',on_delete=models.CASCADE)               #角色ID
    function = models.ForeignKey('BaseFuntion',on_delete=models.CASCADE)    #功能ID

#用户表
class UserInfo(models.Model):
    username = models.CharField(unique=True, max_length=30)                 #用户名/unique=True表示该字段具有唯一性
    password = models.CharField(max_length=30)                              #用户密码
    staffname = models.CharField(max_length=30)                             #用户真实姓名
    email = models.EmailField(null=True, max_length=30)                     #邮箱/null=True表示该字段允许为空
    role = models.ForeignKey('Role',on_delete=models.CASCADE)               #角色，对应角色表
    isenable = models.IntegerField(default=1)                               #是否启用/默认值是1，表示启用

class Host(models.Model):
    hostname = models.CharField(unique=True,max_length=50)                              #服务器名字
    ip = models.CharField(max_length=50)                                    #服务器IP
    remarks = models.CharField(null=True, max_length=500)                   #备注信息

class ParentProject(models.Model):
    projectname = models.CharField(unique=True,max_length=50)                #项目名字
    remarks = models.CharField(null=True, max_length=500)                   #备注信息

class Subproject(models.Model):
    projectname = models.CharField(unique=True,max_length=50)                   # 项目名字
    projectaddress = models.CharField(max_length=100)                           #项目地址
    ParentProject = models.ForeignKey('ParentProject',on_delete=models.CASCADE) #父项目ID
    remarks = models.CharField(null=True, max_length=500)                       # 备注信息

class ProjectForHost(models.Model):
    host = models.ForeignKey('Host',on_delete=models.CASCADE)                   #角色ID
    project = models.ForeignKey('Subproject',on_delete=models.CASCADE)         #功能ID

#版本发布日志
class VersionList(models.Model):
    host = models.ForeignKey('Host',on_delete=models.CASCADE)                       #服务器
    project = models.ForeignKey('Subproject',on_delete=models.CASCADE)              #项目
    version = models.CharField(null=True,max_length=100)                            #版本信息
    updateTime = models.DateTimeField(auto_now=True)                                #更新时间
    ation = models.CharField(max_length=30)                                         #操作
    user = models.ForeignKey('UserInfo',on_delete=models.CASCADE)                   #发布人
    remarks = models.CharField(null=True,max_length=50)                             #备注信息

#配置日志
class AtionLogs(models.Model):
    updateTime = models.DateTimeField(auto_now=True)                        #操作时间
    user = models.ForeignKey('UserInfo',on_delete=models.CASCADE)           #操作人
    ationlog = models.CharField(max_length=100)                            #执行的操作