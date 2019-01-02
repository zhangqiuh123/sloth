from django.shortcuts import render, HttpResponse,redirect
from django.db import connection
from MySite import Sql,models,Login,FunCtionModels
import time

#用户列表
def UserList(request):
    #取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist,staffname,userid = Login.RoleVerify(username)
    #进行用户列表的获取及刷新
    cursor = connection.cursor()
    cursor.execute(Sql.SqlForUser)
    user_list = cursor.fetchall()
    #获取页码
    page = request.GET.get('page', 1)
    #分页，每页15条数据
    user_list = FunCtionModels.paging(user_list,15,page)
    #跳转到用户列表页面
    return render(request, 'UserList.html',{'function': functionlist, 'othersystemlist': othersystemlist, 'username': staffname,"user_list":user_list})

#用户搜索
def SelectUser(request):
    #取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist,staffname,userid = Login.RoleVerify(username)
    #获取搜索内容
    content = request.GET.get('search')
    #搜索的SQL
    cursor = connection.cursor()
    SqlForSelectUser = "SELECT MySite_userinfo.id," \
                       "MySite_userinfo.staffname," \
                       "MySite_userinfo.username," \
                       "MySite_userinfo.email," \
                       "MySite_role.rolename," \
                       " CASE WHEN MySite_userinfo.isenable=1 THEN '启用'  ELSE '禁用' END" \
                       " FROM MySite_userinfo INNER JOIN MySite_role ON MySite_userinfo.role_id = MySite_role.id" \
                       " WHERE MySite_userinfo.staffname LIKE '%%%s%%'"\
                       " OR MySite_userinfo.username LIKE '%%%s%%'" \
                       " OR MySite_role.rolename LIKE '%%%s%%'" % (content,content,content)
    cursor.execute(SqlForSelectUser)
    user_list = cursor.fetchall()
    #获取页码
    page = request.GET.get('page', 1)
    #分页，每页15条数据
    user_list = FunCtionModels.paging(user_list,15,page)
    return render(request, 'UserList.html',{'function': functionlist, 'othersystemlist': othersystemlist, 'username': staffname,"user_list": user_list,"content":content})

#用户添加跳转
def AddUser(request):
    # 取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist, staffname, userid = Login.RoleVerify(username)
    #获取角色信息
    role = Sql.role
    #跳转至添加用户界面
    return render(request, 'AddUser.html',{'function': functionlist, 'othersystemlist': othersystemlist, 'username': staffname,"role":role})

#新增用户界面
def ToAddUser(request):
    if request.method == 'POST':
        #获取用户相关数据
        username = request.session.get('USERNAME', False)
        user = models.UserInfo.objects.get(username=username)
        username_add = request.POST.get('username')
        password = request.POST.get('password')
        staffname_add = request.POST.get('staffname')
        email = request.POST.get('email')
        isclose = request.POST.get('isclose')
        role = request.POST.get('role')

        #判断是否启用
        if isclose == 'on':
            isenable = 1
        else:
            isenable = 0
        #判断用户名是否已经存在
        user_exists = models.UserInfo.objects.filter(username__exact=username_add)
        #获取角色信息
        roles = models.Role.objects.get(rolename=role)
        #如果用户存在则需要重新填写，否则进行用户创建
        if user_exists:
            return HttpResponse("{\"code\":\"用户已存在!\"}")
        else:
            #添加用户信息，写入日志，并跳转至用户列表
            models.UserInfo.objects.create(username=username_add,password=password,staffname=staffname_add,email=email,isenable=isenable,role_id=roles.id)
            NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            ation = '新增了用户: %s'%staffname_add
            models.AtionLogs.objects.create(updateTime=NowTime, ationlog=ation, user_id=user.id)
            return HttpResponse("{\"code\":\"用户创建成功!\"}")
            #return redirect('/index/UserConfig/')

#跳转至用户编辑表单
def UpdateUser(request):
    #取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist,staffname,userid = Login.RoleVerify(username)
    #获取用户相关信息
    userid = request.GET.get('userid')
    user = models.UserInfo.objects.get(id = userid)
    roleid = user.role_id
    isenable = user.isenable
    #如果启用则返回on-启用，否则返回off-禁用
    if isenable == 1:
        isclose = 'true'
    else:
        isclose = 'false'
    #获取角色相关信息
    role = models.Role.objects.get(id = roleid)
    #角色列表
    rolelist = Sql.role
    #跳转至用户更新页面
    return render(request, 'UpdateUser.html',{'function': functionlist, 'othersystemlist': othersystemlist, "user":user,'username': staffname,"role": rolelist,"rolename":role.rolename,"isclose":isclose})

#跳转至编辑自己资料的表单
def UpdateUserForSelf(request):
    #取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist,staffname,userid = Login.RoleVerify(username)
    #获取用户相关信息
    user = models.UserInfo.objects.get(username=username)
    roleid = user.role_id
    isenable = user.isenable
    # 如果启用则返回on-启用，否则返回off-禁用
    if isenable == 1:
        isclose = 'true'
    else:
        isclose = 'false'
    # 获取角色相关信息
    role = models.Role.objects.get(id=roleid)
    # 角色列表
    rolelist = Sql.role
    #跳转至用户编辑界面
    return render(request, 'UpdateUserForSelf.html',{'function': functionlist, 'othersystemlist': othersystemlist, 'username': staffname,"user":user,"role": rolelist, "rolename": role.rolename, "isclose": isclose})

#编辑用户表单
def ToUpdateUser(request):
    # 取得cookie
    username = request.session.get('USERNAME', False)
    #通过cookie进行用户更新
    users = models.UserInfo.objects.get(username=username)
    #从表单获取用户相关信息
    userid = request.POST.get('userid')
    username = request.POST.get('username')
    password = request.POST.get('password')
    staffname_add = request.POST.get('staffname')
    email = request.POST.get('email')
    isclose = request.POST.get('isclose')
    role = request.POST.get('role')
    #判断是否启用
    if isclose == 'on':
        isenable = 1
    else:
        isenable = 0
    #获取角色相关信息
    roles = models.Role.objects.get(rolename=role)
    #获取用户相关信息
    user = models.UserInfo.objects.get(id = userid)
    #被编辑的用户
    usernameberupdate = user.staffname
    #进行用户数据的更新
    user.username=username
    user.password=password
    user.staffname=staffname_add
    user.isenable=isenable
    user.email = email
    user.role_id=roles.id
    user.save()
    #写入日志
    NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    ation = '编辑了用户: %s' %usernameberupdate
    models.AtionLogs.objects.create(updateTime=NowTime, ationlog=ation, user_id=users.id)
    #跳转至用户列表
    return HttpResponse("{\"code\":\"版本修改成功!\"}")
    #return redirect('/index/UserConfig/')

#编辑自己资料表单
def ToUpdateUserForSelf(request):
    #获取cookie，并通过cookie获取用户相关信息
    username = request.session.get('USERNAME', False)
    user = models.UserInfo.objects.get(username=username)
    #从前端获取密码，用户名及email
    password = request.POST.get('password')
    staffname_add = request.POST.get('staffname')
    email = request.POST.get('email')
    #更新用户相关信息
    user.password=password
    user.staffname=staffname_add
    user.email = email
    user.save()
    #写入日志并跳转至首页
    NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    ation = '编辑了用户: %s' % user.staffname
    models.AtionLogs.objects.create(updateTime=NowTime, ationlog=ation, user_id=user.id)
    return HttpResponse("{\"code\":\"用户编辑成功!\"}")
    #return redirect('/index/')

#删除用户
def DelUser(request):
    #获取cookie，并通过cookie获取用户相关信息
    username = request.session.get('USERNAME', False)
    users = models.UserInfo.objects.get(username=username)
    #从前端获取需要删除用户的id并获取用户相关信息
    userid = request.GET.get('userid')
    user = models.UserInfo.objects.get(id = userid)
    #写入日志并删除用户
    NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    ation = '删除了用户: %s' % user.staffname
    models.AtionLogs.objects.create(updateTime=NowTime, ationlog=ation, user_id=users.id)
    user.delete()
    #跳转至用户列表
    return redirect('/index/UserConfig/')

#跳转至修改密码页面
def UpdatePassword(request):
    #取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist,staffname,userid = Login.RoleVerify(username)
    #跳转至修改密码界面
    return render(request, 'UpdatePassword.html',{'function': functionlist, 'othersystemlist': othersystemlist, 'username': staffname})

#修改密码表单
def ToUpdatePassword(request):
    # 获取cookie，并通过cookie获取用户相关信息
    username = request.session.get('USERNAME', False)
    user = models.UserInfo.objects.get(username=username)
    #从前端获取密码相关信息
    oldpassword = request.POST.get('OldPassword')
    newpassword = request.POST.get('NewPassword')
    newpasswordagain = request.POST.get('NewPasswordAgain')

    passwd = models.UserInfo.objects.filter(username__exact=username,password__exact=oldpassword)

    if passwd:
        if newpassword == newpasswordagain:
            user.password = newpasswordagain
            user.save()
            #跳转至用户登录界面
            return HttpResponse("{\"code\":\"密码已修改!\"}")
            #return redirect('/LoginOut/')
        else:
            return HttpResponse("{\"code\":\"两次输入的密码不一致!\"}")
    else:
        return HttpResponse("{\"code\":\"你输入的密码不正确!\"}")
