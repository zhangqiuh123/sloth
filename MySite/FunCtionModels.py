from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db import connection

#分页函数，传三个参数，需要分页处理的数据列表，每页数据条数和页码
def paging(list,num,page):
    paginator = Paginator(list,num)
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    #返回分页后的数据
    return list

#瑞鹏ERP/HIS系统、微服务相关、瑞鹏宠医云相关功能列表及URL
def otherSystem(description):
    cursor = connection.cursor()
    SqlForFunction = "SELECT functionname,remarks,functionurl FROM MySite_basefuntion WHERE description = '%s'"%description

    cursor.execute(SqlForFunction)
    function_list = cursor.fetchall()

    return function_list
