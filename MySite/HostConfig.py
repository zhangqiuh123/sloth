from django.shortcuts import render, HttpResponse,redirect
from django.db import connection
from MySite import Sql,models,Login,FunCtionModels
import time

#列出主机列表
def HostList(request):
    # 取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist,staffname,userid = Login.RoleVerify(username)
    #刷新主机列表
    cursor = connection.cursor()
    cursor.execute(Sql.SqlForHostList)
    host_list = cursor.fetchall()
    #获取页码
    page = request.GET.get('page', 1)
    # 分页，每页10条数据
    host_list = FunCtionModels.paging(host_list,15,page)
    #跳转到主机列表
    return render(request, 'HostList.html',{'function': functionlist, 'othersystemlist': othersystemlist, 'username': staffname,"host_list":host_list})

#主机搜索
def SelectHost(request):
    # 取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist,staffname,userid = Login.RoleVerify(username)
    #获取搜索内容
    content = request.GET.get('search')
    #搜索主机相关SQL
    cursor = connection.cursor()
    SqlForSelectHost = "SELECT * FROM mysite_host WHERE hostname LIKE '%%%s%%' OR ip LIKE '%%%s%%'"%(content,content)
    cursor.execute(SqlForSelectHost)
    host_list = cursor.fetchall()
    #获取页码
    page = request.GET.get('page', 1)
    # 分页，每页10条数据
    host_list = FunCtionModels.paging(host_list,15,page)
    #跳转到主机列表
    return render(request, 'HostList.html',{'function': functionlist, 'othersystemlist': othersystemlist, 'username': staffname,"host_list": host_list})

#跳转至添加主机表单
def AddHost(request):
    # 取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist,staffname,userid = Login.RoleVerify(username)
    #跳转到添加主机表单
    return render(request, 'AddHost.html',{'function': functionlist, 'othersystemlist': othersystemlist, 'username': staffname})

#添加主机
def ToAddHost(request):
    if request.method == 'POST':
        #取得cookie，并根据cookie获取用户
        username = request.session.get('USERNAME', False)
        user = models.UserInfo.objects.get(username=username)
        #从前端获取主机信息
        hostname = request.POST.get('hostname')
        ip = request.POST.get('ip')
        remark = request.POST.get('desc')
        #判断主机是否存在
        host_exists = models.Host.objects.filter(hostname__exact=hostname)
        if host_exists:
            return HttpResponse("{\"code\":\"该主机已存在!\"}")
        else:
            #创建主机并写入日志，然后跳转到主机列表
            models.Host.objects.create(hostname=hostname,ip=ip,remarks=remark)
            NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            ation = '新增了角色: %s'%hostname
            models.AtionLogs.objects.create(updateTime=NowTime, ationlog=ation, user_id=user.id)
            #return redirect('/index/HostConfig/')
            return HttpResponse("{\"code\":\"主机已成功添加!\"}")

#跳转至更新主机页面
def UpdateHost(request):
    # 取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist,staffname,userid = Login.RoleVerify(username)
    #根据主机Id,将主机信息返回给前端
    hostid = request.GET.get('hostid')
    host = models.Host.objects.get(id=hostid)
    #跳转至更新主机的表单
    return render(request, 'UpdateHost.html',{'function': functionlist, 'othersystemlist': othersystemlist, 'username': staffname,"host":host})

#更新主机信息
def ToUpdateHost(request):
    #取得cookie并根据cookie获取用户
    username = request.session.get('USERNAME', False)
    user = models.UserInfo.objects.get(username=username)
    #从前端获取主机相关信息
    hostid = request.POST.get('hostid')
    hostname = request.POST.get('hostname')
    ip = request.POST.get('ip')
    remark = request.POST.get('desc')
    #根据id获取主机，并对该主机进行数据更新
    host = models.Host.objects.get(id=hostid)
    hostnamebeupdate = host.hostname
    host.hostname = hostname
    host.ip = ip
    host.remarks = remark
    host.save()
    #写入日志并跳转至主机列表
    NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    ation = '编辑了主机: %s' % hostnamebeupdate
    models.AtionLogs.objects.create(updateTime=NowTime, ationlog=ation, user_id=user.id)
    #return redirect('/index/HostConfig/')
    return HttpResponse("{\"code\":\"主机已经修改!\"}")

def DelHost(request):
    #取得cookie并根据cookie获取用户信息
    username = request.session.get('USERNAME', False)
    user = models.UserInfo.objects.get(username=username)
    #根据前端返回的主机Id获取主机
    hostid = request.GET.get('hostid')
    host = models.Host.objects.get(id=hostid)
    #写入日志
    NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    ation = '删除了主机: %s' % host.hostname
    models.AtionLogs.objects.create(updateTime=NowTime, ationlog=ation, user_id=user.id)
    host.delete()
    #删除后跳转至主机列表
    return redirect('/index/HostConfig/')