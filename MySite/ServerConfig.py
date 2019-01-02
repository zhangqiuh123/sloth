from django.shortcuts import render
from django.db import connection
from MySite import List,Sql,models
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def ServerList(request):
    sql = Sql.SqlStatement()
    functionlist = List.List().function_list
    othersystemlist = List.List().other_system_list
    username = request.session.get('USERNAME', False)
    user = models.UserInfo.objects.get(username=username)

    cursor = connection.cursor()
    cursor.execute(sql.SqlForHost)
    host_list = cursor.fetchall()

    paginator = Paginator(host_list,3)
    page = request.GET.get('page',1)

    try:
        host_list = paginator.page(page)
    except PageNotAnInteger:
        host_list = paginator.page(1)
    except EmptyPage:
        host_list = paginator.page(paginator.num_pages)

    hostlist = List.List().hostlist
    paginator = Paginator(hostlist, 10)
    page = request.GET.get('page', 1)

    try:
        hostlist = paginator.page(page)
    except PageNotAnInteger:
        hostlist = paginator.page(1)
    except EmptyPage:
        hostlist = paginator.page(paginator.num_pages)


    hlist = host_list[0]

    SqlForAddress = "SELECT ip FROM mysite_host WHERE hostname='%s'" % hlist
    cursor.execute(SqlForAddress)
    result_address = cursor.fetchall()

    SqlForHostID = "SELECT id FROM mysite_host WHERE hostname='%s'" % hlist
    cursor.execute(SqlForHostID)
    result_host = cursor.fetchall()


    hostid = result_host[0]

    SqlForproject = "SELECT  MySite_subproject.projectname FROM MySite_subproject " \
                    " INNER JOIN MySite_projectforhost ON MySite_subproject.id = MySite_projectforhost.project_id" \
                    " WHERE MySite_projectforhost.host_id = %d" % hostid


    cursor.execute(SqlForproject)
    project_list = cursor.fetchall()

    #project_list ='a'


    return render(request, 'ServerConfig.html',{'function': functionlist, 'othersystemlist': othersystemlist, 'username': user.staffname,"host_list": host_list,"hostlist":hostlist, "project_list": result_host,"address":result_address})