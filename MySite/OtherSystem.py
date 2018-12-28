from django.shortcuts import render
from MySite import Sql,Login,FunCtionModels

#瑞鹏ERP/HIS系统 站点及链接界面
def RuiPengErpAndHis(request):
    # 取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist,staffname,userid = Login.RoleVerify(username)
    #判断属于哪个页面，并获取相关主机列表
    description = '瑞鹏ERP/HIS系统'
    function_list = FunCtionModels.otherSystem(description)
    #获取页码
    page = request.GET.get('page', 1)
    #分页，每页3条数据
    function_list = FunCtionModels.paging(function_list,3,page)
    #跳转到瑞鹏ERP/HIS系统，站点及链接界面
    return render(request,'RuiPengErpAndHis.html',{'function': functionlist, 'othersystemlist': othersystemlist, 'username': staffname,"OtherSystem_list_URL":function_list})

#微服务相关 站点及链接界面
def RuiPengMicroservice(request):
    # 取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist, staffname, userid = Login.RoleVerify(username)
    # 判断属于哪个页面，并获取相关主机列表
    description = '微服务相关'
    function_list = FunCtionModels.otherSystem(description)
    # 获取页码
    page = request.GET.get('page', 1)
    # 分页，每页3条数据
    function_list = FunCtionModels.paging(function_list, 3, page)
    # 跳转到微服务相关，站点及链接界面
    return render(request, 'RuiPengMicroservice.html',{'function': functionlist, 'othersystemlist': othersystemlist, 'username': staffname,"OtherSystem_list_URL": function_list})

#瑞鹏宠医云 站点及链接界面
def RuiPengApp(request):
    # 取得cookie并进行角色权限验证
    username = request.session.get('USERNAME', False)
    functionlist, othersystemlist, staffname, userid = Login.RoleVerify(username)
    # 判断属于哪个页面，并获取相关主机列表
    description = '瑞鹏宠医云'
    function_list = FunCtionModels.otherSystem(description)
    # 获取页码
    page = request.GET.get('page', 1)
    # 分页，每页3条数据
    function_list = FunCtionModels.paging(function_list, 3, page)
    # 跳转到瑞鹏宠医云，站点及链接界面
    return render(request, 'RuiPengApp.html',{'function': functionlist, 'othersystemlist': othersystemlist, 'username': staffname,"OtherSystem_list_URL": function_list})
