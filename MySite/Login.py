from django.db import connection, transaction
from MySite import models
from django.shortcuts import render
import time

#验证角色
def RoleVerify(username):
    #根据传参进行搜索搜索
    user = models.UserInfo.objects.get(username=username)
    #根据用户角色ID进行功能菜单权限的验证
    SqlForFuntionList = "SELECT MySite_basefuntion.functionname,MySite_basefuntion.functionurl FROM MySite_basefuntion " \
                        " INNER JOIN MySite_funtionrole ON MySite_basefuntion.id=MySite_funtionrole.function_id" \
                        " WHERE description = '功能菜单'" \
                        " AND MySite_funtionrole.role_id=%d " % user.role_id
    # 根据用户角色ID进行其他系统权限的验证
    SqlForOtherSystem = "SELECT MySite_basefuntion.functionurl," \
                        "MySite_basefuntion.isnewview," \
                        "MySite_basefuntion.functionname FROM MySite_basefuntion" \
                        " INNER JOIN MySite_funtionrole ON MySite_basefuntion.id=MySite_funtionrole.function_id" \
                        " WHERE description = '其他系统'" \
                        " AND MySite_funtionrole.role_id=%d " % user.role_id
    cursor = connection.cursor()
    cursor.execute(SqlForOtherSystem)
    othersystemlist = cursor.fetchall()
    cursor = connection.cursor()
    cursor.execute(SqlForFuntionList)
    functionlist = cursor.fetchall()
    #获取用户姓名和用户ID
    staffname = user.staffname
    userid = user.id
    #返回功能菜单列表，其他系统列表，用户姓名及用户ID
    return functionlist,othersystemlist,staffname,userid

#返回主页
def islogin(request):
    #获取cookie，并执行函数进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist,staffname,userid = RoleVerify(username)
    #写入日志
    NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    models.AtionLogs.objects.create(updateTime=NowTime, ationlog='登录系统', user_id=userid)
    return render(request, 'index.html',{'function': functionlist, 'othersystemlist': othersystemlist, 'username': staffname})