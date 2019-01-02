from django.shortcuts import render, HttpResponse,redirect
from django.db import connection
from MySite import Sql,models,Login,FunCtionModels
import time

#角色列表
def RoleList(request):
    #取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist,staffname,userid = Login.RoleVerify(username)
    #刷新角色列表
    cursor = connection.cursor()
    cursor.execute(Sql.SqlForRoleList)
    role_list = cursor.fetchall()
    # 获取页码
    page = request.GET.get('page', 1)
    # 分页，每页15条数据
    role_list = FunCtionModels.paging(role_list, 15, page)
    #跳转至角色列表页面
    return render(request, 'RoleList.html',{'function': functionlist, 'othersystemlist': othersystemlist, 'username': staffname,"role_list":role_list})

#搜索角色
def SelectRole(request):
    #取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist,staffname,userid = Login.RoleVerify(username)
    #获取搜索的内容
    content = request.GET.get('search')
    #搜索角色的SQL
    cursor = connection.cursor()
    SqlForSelectRole = "SELECT MySite_role.id," \
                       "MySite_role.rolename," \
                       " CASE WHEN MySite_role.isenable=1 THEN '启用'  ELSE '禁用' END," \
                       " MySite_role.remarks " \
                       " FROM MySite_role where MySite_role.rolename like '%%%s%%'"%content
    cursor.execute(SqlForSelectRole)
    role_list = cursor.fetchall()
    # 获取页码
    page = request.GET.get('page', 1)
    # 分页，每页15条数据
    role_list = FunCtionModels.paging(role_list, 15, page)
    #跳转至角色列表
    return render(request, 'RoleList.html',{'function': functionlist, 'othersystemlist': othersystemlist, 'username': staffname,"role_list": role_list})

#跳转至角色添加表单
def AddRole(request):
    #取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist,staffname,userid = Login.RoleVerify(username)
    #获取可用权限配置列表
    function_list = Sql.funtionList()
    #跳转至角色添加页面
    return render(request, 'AddRole.html',{'function': functionlist,'function_list':function_list,'othersystemlist': othersystemlist, 'username': staffname})

#角色添加表单
def ToAddRole(request):
    if request.method == 'POST':
        username = request.session.get('USERNAME', False)
        user = models.UserInfo.objects.get(username=username)
        #从前端获取角色相关信息
        rolename = request.POST.get('rolename')
        remark = request.POST.get('desc')
        isclose = request.POST.get('close')

        #判断是否启用，on表示启用，其他表示不启用
        if isclose == 'on':
            isenable = 1
        else:
            isenable = 0
        #判断角色是否存在
        role_exists = models.Role.objects.filter(rolename__exact=rolename)
        if role_exists:
            return HttpResponse("{\"code\":\"角色已存在!\"}")
        else:
            #更新角色信息
            models.Role.objects.create(rolename=rolename,isenable=isenable,remarks=remark)
            #更新角色权限对应表
            functionid = Sql.functionid
            role = models.Role.objects.get(rolename=rolename)
            for funid in functionid:
                fun = 'A' + '%d'%funid
                funname = request.POST.get(fun)
                if funname == 'on':
                    models.FuntionRole.objects.create(function_id=funid,role_id=role.id)
            #写入日志并跳转到角色列表
            NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            ation = '新增了角色: %s'%rolename
            models.AtionLogs.objects.create(updateTime=NowTime, ationlog=ation, user_id=user.id)
            #return redirect('/index/RoleConfig/')
            return HttpResponse("{\"code\":\"角色创建成功!\"}")

#跳转至角色编辑页面
def UpdateRole(request):
    # 取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist,staffname,userid = Login.RoleVerify(username)
    #从前端获取角色ID
    roleid = request.GET.get('roleid')
    #根据角色ID获取角色信息
    role = models.Role.objects.get(id=roleid)
    isenable = role.isenable
    #获取该角色具备的权限列表
    function_list = Sql.funtion_List(roleid)
    #判断是否启用
    if isenable == 1:
        isclose = 'true'
    else:
        isclose = 'false'
    #跳转至更新角色页面
    return render(request, 'UpdateRole.html',{'function': functionlist, 'othersystemlist': othersystemlist,'function_list':function_list, 'username': staffname,"role":role,"isclose":isclose})

def ToUpdateRole(request):
    #从前端页面获取相关信息
    username = request.session.get('USERNAME', False)
    user = models.UserInfo.objects.get(username=username)
    roleid = request.POST.get('roleid')
    rolename = request.POST.get('rolename')
    remark = request.POST.get('desc')
    isclose = request.POST.get('isclose')
    #判断是否启用，on为启用，其他为不启用
    if isclose == 'on':
        isenable = 1
    else:
        isenable = 0
    #获取功能列表
    functionid = Sql.functionid
    #获取角色相关信息
    role = models.Role.objects.get(rolename=rolename)
    #进行功能角色对应表的更新，遍历所有功能列表ID，从前端取值判断是否启用
    for funid in functionid:
        fun = 'A' + '%d' % funid
        #从前端取值
        funname = request.POST.get(fun)
        #判断是否启用
        if funname == 'on':
            #判断表中是否存在相关数据
            function_exists = models.FuntionRole.objects.filter(function_id__exact=funid,role_id__exact=role.id)
            if function_exists:
                print("......")
            else:
                models.FuntionRole.objects.create(function_id=funid,role_id=role.id)
        #如果状态为不启用，则删除相关的数据
        else:
            models.FuntionRole.objects.filter(function_id__exact=funid,role_id__exact=role.id).delete()

    #更新角色相关数据
    role = models.Role.objects.get(id = roleid)
    rolenamebeupdate = role.rolename
    role.rolename = rolename
    role.isenable = isenable
    role.remarks = remark
    role.save()
    #写入日志，并跳转到角色主界面
    NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    ation = '编辑了角色: %s' % rolenamebeupdate
    models.AtionLogs.objects.create(updateTime=NowTime, ationlog=ation, user_id=user.id)
    #return redirect('/index/RoleConfig/')
    return HttpResponse("{\"code\":\"角色已经修改!\"}")

def DelRole(request):
    # 取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist,staffname,userid = Login.RoleVerify(username)
    cursor = connection.cursor()
    #从前端获取角色ID
    roleid = request.GET.get('roleid')
    #根据角色ID获取角色信息
    role = models.Role.objects.get(id = roleid)
    #删除角色相关联功能权限
    SqlForDelFunctionRole = "DELETE FROM MySite_funtionrole WHERE role_id = %d "%role.id
    cursor.execute(SqlForDelFunctionRole)
    #写入日志并删除角色数据
    NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    ation = '删除了角色: %s' % role.rolename
    models.AtionLogs.objects.create(updateTime=NowTime, ationlog=ation, user_id=userid)
    role.delete()
    #跳转至角色列表
    return redirect('/index/RoleConfig/')