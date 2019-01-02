"""sloth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MySite import views,VersionUpdate,VersionListViews,VersionSync,MicroserviceConfig
from MySite import Login,AtionLogs,UserConfig,OtherSystem,RoleConfig,HostConfig

urlpatterns = [
    #用户登录相关
    path('', views.login),
    path('islogin/', views.index),
    path('index/',Login.islogin),
    path('LoginOut/', views.LoginExit),
    #用户版本列表相关
    path('index/VersionList/', VersionListViews.VersionList),
    path('index/VersionList/VersionSelect/', VersionListViews.VersionSelect),
    #用户版本更新同步与回退相关
    path('index/MainVersionConfig/', VersionUpdate.VersionMainList),
    path('index/VersionList/UpdateVersion/', VersionUpdate.UpdateVersion),
    path('index/VersionList/ToVersionUpdate/', VersionUpdate.ToVersionUpdate),
    path('index/VersionList/VersionUpdate/', VersionUpdate.VersionUpdate),
    path('index/VersionSync/', VersionSync.VersionOtherList),
    path('index/MicroserviceConfig/', MicroserviceConfig.MicroserviceList),
    #用户管理相关
    path('index/UserConfig/', UserConfig.UserList),
    path('index/UserConfig/AddUser/', UserConfig.AddUser),
    path('index/UserConfig/ToAddUser/', UserConfig.ToAddUser),
    path('index/UserConfig/DelUser/', UserConfig.DelUser),
    path('index/UserConfig/UpdateUser/', UserConfig.UpdateUser),
    path('index/UserConfig/UpdateUserForSelf/', UserConfig.UpdateUserForSelf),
    path('index/UserConfig/ToUpdateUser/', UserConfig.ToUpdateUser),
    path('index/UserConfig/ToUpdateUserForSelf/', UserConfig.ToUpdateUserForSelf),
    path('index/UserConfig/SelectUser/', UserConfig.SelectUser),
    path('index/UserConfig/UpdatePassword/', UserConfig.UpdatePassword),
    path('index/UserConfig/ToUpdatePassword/', UserConfig.ToUpdatePassword),
    #角色管理相关
    path('index/RoleConfig/',RoleConfig.RoleList ),
    path('index/RoleConfig/AddRole/', RoleConfig.AddRole),
    path('index/RoleConfig/ToAddRole/', RoleConfig.ToAddRole),
    path('index/RoleConfig/DelRole/', RoleConfig.DelRole),
    path('index/RoleConfig/UpdateRole/', RoleConfig.UpdateRole),
    path('index/RoleConfig/ToUpdateRole/', RoleConfig.ToUpdateRole),
    path('index/RoleConfig/SelectRole/', RoleConfig.SelectRole),
    #主机管理相关
    path('index/HostConfig/', HostConfig.HostList),
    path('index/HostConfig/AddHost/', HostConfig.AddHost),
    path('index/HostConfig/ToAddHost/', HostConfig.ToAddHost),
    path('index/HostConfig/DelHost/', HostConfig.DelHost),
    path('index/HostConfig/UpdateHost/', HostConfig.UpdateHost),
    path('index/HostConfig/ToUpdateHost/', HostConfig.ToUpdateHost),
    path('index/HostConfig/SelectHost/', HostConfig.SelectHost),
    #操作日志
    path('index/AtionLogs/', AtionLogs.AtionLogs),
    #其他系统链接相关
    path('index/OtherSystem/RuiPengErpAndHis/', OtherSystem.RuiPengErpAndHis),
    path('index/OtherSystem/RuiPengMicroservice/', OtherSystem.RuiPengMicroservice),
    path('index/OtherSystem/RuiPengApp/', OtherSystem.RuiPengApp),
]