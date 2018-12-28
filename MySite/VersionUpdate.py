from django.shortcuts import render,HttpResponse,redirect
from MySite import Sql,models,Login,FunCtionModels
import time,socket
from urllib import parse

#连接Windows服务器执行批处理的套接字函数
def send_cmd(ipaddr, instr):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ipaddr, 18432))
        client.settimeout(5)
        client.sendall(parse.quote(instr).encode('utf-8'))
    except Exception as e:
        print(e)
    finally:
        client.close()

#列出版本列表
def VersionMainList(request):
    # 取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    user = models.UserInfo.objects.get(username=username)
    functionlist, othersystemlist,staffname,userid = Login.RoleVerify(username)
    #完成版本列表刷新的操作
    ParentProjectid = 1
    versionlog_list, host_list, project_list = Sql.SqlForVersionLog(ParentProjectid)
    #做主机权限的更改
    if user.role_id == 1 or user.role_id == 2:
        host_list = host_list[0:3]
    elif user.role_id > 2 and user.role_id < 6:
        host_list = host_list[0:2]
    else:
        host_list = host_list[0:1]

    #获取页码
    page = request.GET.get('page', 1)
    # 分页，每页15条数据
    versionlog_list = FunCtionModels.paging(versionlog_list,15,page)
    #返回主页
    return render(request, 'VersionUpdate.html',{'function': functionlist, 'othersystemlist': othersystemlist, 'username': staffname,"project_list": project_list,"versionlog_list": versionlog_list,"host_list": host_list})

#获取主机和项目的值，并跳转到版本更新页面UpdateVersion.html
def UpdateVersion(request):
    # 取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist,staffname,userid = Login.RoleVerify(username)
    #获取主机和项目
    host = request.GET.get('host')
    project = request.GET.get('project')
    #跳转到版本发布页面
    return render(request, 'UpdateVersion.html',{'function': functionlist, 'othersystemlist': othersystemlist, 'username': staffname,"host":host,"project":project})

#进行版本更新
def ToVersionUpdate(request):
    # 取得cookie
    username = request.session.get('USERNAME', False)
    user = models.UserInfo.objects.get(username=username)

    if request.method == 'POST':
        #从表单获取相关信息
        hostname = request.POST.get('host')
        projectname = request.POST.get('project')
        version = request.POST.get('version')
        remarks = request.POST.get('desc')

        #获取主机信息
        host = models.Host.objects.get(hostname=hostname)
        #验证版本是否存在
        version_exists = models.VersionList.objects.filter(version__iexact=version)
        #获取项目信息
        project = models.Subproject.objects.get(projectname=projectname)
        #定义脚本名字
        a = projectname
        b = "update.bat"
        msg_update = a + b

        #判断版本是否存在
        if version_exists:
            return HttpResponse("{\"code\":\"该版本号已存在，请重新输入!\"}")
        else:
            #进行版本发布，并写入日志
            send_cmd(host.ip, msg_update)
            NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            models.VersionList.objects.create(updateTime=NowTime,ation='版本发布',remarks=remarks,project_id=project.id,host_id=host.id,user_id=user.id,version=version)
            ation = '进行了版本发布，更新的服务器是：%s ,项目是：%s，版本是：%s'%(hostname,projectname,version)
            models.AtionLogs.objects.create(updateTime=NowTime,ationlog=ation,user_id=user.id)
            return HttpResponse("{\"code\":\"版本发布成功!\"}")
            #return redirect('/index/MainVersionConfig/')

#版本同步与回退
def VersionUpdate(request):
    #获取相关信息
    if request.method == 'POST':
        hostname = request.POST.get('host')
        projectname = request.POST.get('project')
        type = request.POST.get('type')
        username = request.session.get('USERNAME', False)
        user = models.UserInfo.objects.get(username=username)
        host = models.Host.objects.get(hostname=hostname)
        project = models.Subproject.objects.get(projectname=projectname)
        #定义脚本名字
        a = project.projectname
        b = "update.bat"
        c = "rollback.bat"
        msg_update = a + b
        msg_rollback = a + c

        #版本同步与版本回退，原理与版本发布一致，只不过少了一个表单
        if type == 'sysnc':
            remarkforsync = '更新到最新版本'
            send_cmd(host.ip,msg_update)
            NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            models.VersionList.objects.create(updateTime=NowTime,ation='版本同步',remarks=remarkforsync,project_id=project.id,host_id=host.id,user_id=user.id,version='最新版本')
            ation = '进行了版本同步，更新的服务器是：%s ,项目是：%s'%(hostname,projectname)
            models.AtionLogs.objects.create(updateTime=NowTime,ationlog=ation,user_id=user.id)
            return HttpResponse("{\"code\":\"版本同步成功!\"}")
        elif type == 'rollback':
            remarkforrollback = '回到到昨天的版本'
            send_cmd(host.ip,msg_rollback)
            NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            models.VersionList.objects.create(updateTime=NowTime,ation='版本回退',remarks=remarkforrollback,project_id=project.id,host_id=host.id,user_id=user.id,version='昨天的版本')
            ation = '进行了版本回退，更新的服务器是：%s ,项目是：%s'%(hostname,projectname)
            models.AtionLogs.objects.create(updateTime=NowTime,ationlog=ation,user_id=user.id)
            return HttpResponse("{\"code\":\"版本回退成功!\"}")






