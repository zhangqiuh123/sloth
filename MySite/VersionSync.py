from django.shortcuts import render
from MySite import Sql,Login,FunCtionModels

#其他系统版本列表，包括佳雯，爱玩乐和东方
def VersionOtherList(request):
    #取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist,staffname,userid = Login.RoleVerify(username)
    #更新版本列表
    ParentProjectid = 4
    versionlog_list, host_list, project_list = Sql.SqlForVersionLog(ParentProjectid)
    #获取页码
    page = request.GET.get('page', 1)
    # 分页，每页15条数据
    versionlog_list = FunCtionModels.paging(versionlog_list,15,page)
    #跳转到版本列表界面
    return render(request, 'VersionSync.html',{'function': functionlist, 'othersystemlist': othersystemlist, 'username': staffname,"project_list": project_list, "versionlog_list": versionlog_list, "host_list": host_list})