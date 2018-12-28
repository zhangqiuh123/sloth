from django.shortcuts import render
from django.db import connection
from MySite import Sql,Login,FunCtionModels

#版本列表
def VersionList(request):
    # 取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist,staffname,userid = Login.RoleVerify(username)
    #获取主机和项目
    host_list = Sql.host_list
    project_list = Sql.project_list
    #进行版本列表的刷新
    cursor = connection.cursor()
    cursor.execute(Sql.SqlForMainVerListLog)
    versionlog_list = cursor.fetchall()
    #获取页码
    page = request.GET.get('page', 1)
    #分页，每页15条数据
    versionlog_list = FunCtionModels.paging(versionlog_list,15,page)
    #跳转到版本列表界面
    return render(request, 'VersionList.html',{'function': functionlist, 'othersystemlist': othersystemlist,"host_list": host_list,"project_list": project_list, 'username': staffname,"versionlog_list":versionlog_list})

#版本搜索功能
def VersionSelect(request):
    # 取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist,staffname,userid = Login.RoleVerify(username)
    #获取主机和项目列表
    host_list = Sql.hostname_list
    project_list = Sql.project_list
    #从前端页面获取主机和项目信息
    host = request.GET.get('host')
    project = request.GET.get('project')

    #进行判断，如果选择的是all，则搜索条件为like %%，否则为主机或项目本身
    if host == 'all':
        host = '%%'
        if project == 'all':
            project = '%%'
        else:
            project = project
    else:
        host = host
        if project == 'all':
            project = '%%'
        else:
            project = project

    #搜索相关的SQL语句
    cursor = connection.cursor()
    SqlForVerListLogSelect = "SELECT MySite_versionlist.id,MySite_host.hostname," \
                             "MySite_subproject.projectname," \
                             "MySite_versionlist.version," \
                             "MySite_versionlist.updateTime," \
                             "MySite_versionlist.ation," \
                             "MySite_userinfo.staffname," \
                             "MySite_versionlist.remarks" \
                             " FROM MySite_versionlist" \
                             " INNER JOIN MySite_host ON MySite_host.id = MySite_versionlist.host_id" \
                             " INNER JOIN MySite_subproject ON MySite_versionlist.project_id = MySite_subproject.id" \
                             " INNER JOIN MySite_userinfo ON MySite_versionlist.user_id = MySite_userinfo.id" \
                             " WHERE MySite_host.hostname LIKE '%s' AND MySite_subproject.projectname LIKE '%s'" \
                             " ORDER BY MySite_versionlist.updateTime DESC "% (host, project)
    cursor.execute(SqlForVerListLogSelect)
    versionlog_list = cursor.fetchall()
    cursor.close()
    connection.close()

    #获取页码
    page = request.GET.get('page', 1)
    #分页，每页15条数据
    versionlog_list = FunCtionModels.paging(versionlog_list,15,page)
    #跳转到版本列表
    return render(request, 'VersionList.html',{'function': functionlist, 'othersystemlist': othersystemlist, "host_list": host_list,"project_list": project_list, 'username': staffname, "versionlog_list": versionlog_list})