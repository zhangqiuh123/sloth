from django.shortcuts import render
from django.db import connection
from MySite import Sql,Login,FunCtionModels

def AtionLogs(request):
    # 取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist,staffname,userid = Login.RoleVerify(username)
    #获取主机及项目信息
    host_list = Sql.host_list
    project_list = Sql.project_list
    #刷新日志列表
    cursor = connection.cursor()
    cursor.execute(Sql.SqlForAtionLogs)
    AtionLogs_list = cursor.fetchall()
    #获取页码
    page = request.GET.get('page', 1)
    # 分页，每页10条数据
    AtionLogs_list = FunCtionModels.paging(AtionLogs_list,10,page)
    #跳转日志列表界面
    return render(request, 'AtionLogs.html',{'function': functionlist, 'othersystemlist': othersystemlist, 'username': staffname,"project_list": project_list, "AtionLogs_list":AtionLogs_list, "host_list": host_list})