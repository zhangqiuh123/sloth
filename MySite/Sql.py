from django.db import connection

cursor = connection.cursor()

#主机名列表
SqlForHostNameList = "SELECT hostname FROM MySite_host "
cursor.execute(SqlForHostNameList)
hostname_list = cursor.fetchall()

#主机信息列表
SqlForHostList = "SELECT * FROM MySite_host"
cursor.execute(SqlForHostList)
host_list = cursor.fetchall()

#子项目列表
SqlForProject = "SELECT projectname FROM MySite_subproject"
cursor.execute(SqlForProject)
project_list = cursor.fetchall()

#获取角色权限配置相关ID
SqlForFunctionId = "SELECT id FROM MySite_basefuntion WHERE description = '功能菜单' OR description = '其他系统'"
cursor.execute(SqlForFunctionId)
functionid =[]
for row in cursor:
    functionid.append(row[0])


#角色名列表
SqlForRole = "SELECT rolename FROM MySite_role"
cursor.execute(SqlForRole)
role = cursor.fetchall()
#角色列表
SqlForRoleList = "SELECT MySite_role.id," \
                 "MySite_role.rolename," \
                 " CASE WHEN MySite_role.isenable=1 THEN '启用'  ELSE '禁用' END," \
                 " MySite_role.remarks FROM MySite_role"

#版本列表
SqlForMainVerListLog = "SELECT MySite_versionlist.id," \
                   "MySite_host.hostname," \
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
                   " ORDER BY MySite_versionlist.updateTime DESC"

#用户信息列表
SqlForUser = "SELECT MySite_userinfo.id," \
             "MySite_userinfo.staffname," \
             "MySite_userinfo.username," \
             "MySite_userinfo.email," \
             "MySite_role.rolename," \
             " CASE WHEN MySite_userinfo.isenable=1 THEN '启用'  ELSE '禁用' END " \
             " FROM MySite_userinfo " \
             " INNER JOIN MySite_role ON MySite_userinfo.role_id = MySite_role.id"
cursor.execute(SqlForUser)
user_list = cursor.fetchall()

#操作日志
SqlForAtionLogs = "SELECT MySite_ationlogs.updateTime," \
                  "MySite_userinfo.staffname," \
                  "MySite_ationlogs.ationlog" \
                  " FROM MySite_ationlogs" \
                  " INNER JOIN MySite_userinfo" \
                  " ON MySite_ationlogs.user_id = MySite_userinfo.id" \
                  " ORDER BY MySite_ationlogs.updateTime DESC"

#查询其他主机的版本列表、主机列表及项目列表
def SqlForVersionLog(ParentProjectid):
        SqlForVerListMainLog = "SELECT MySite_versionlist.id," \
                               "MySite_host.hostname," \
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
                               " WHERE MySite_subproject.ParentProject_id=%d " \
                               " ORDER BY MySite_versionlist.updateTime DESC"%ParentProjectid

        SqlForErpHost = "SELECT DISTINCT MySite_host.hostname FROM MySite_host " \
                        " INNER JOIN MySite_projectforhost ON MySite_host.id = MySite_projectforhost.host_id" \
                        " INNER JOIN MySite_subproject ON MySite_subproject.id = MySite_projectforhost.project_id" \
                        " WHERE MySite_subproject.ParentProject_id = %d "%ParentProjectid

        SqlForErpProject = "SELECT projectname FROM MySite_subproject WHERE ParentProject_id = %d "%ParentProjectid

        cursor = connection.cursor()
        cursor.execute(SqlForVerListMainLog)
        versionlog_list = cursor.fetchall()

        cursor.execute(SqlForErpHost)
        host_list = cursor.fetchall()

        cursor.execute(SqlForErpProject)
        project_list = cursor.fetchall()

        cursor.close()
        connection.close()

        return versionlog_list,host_list,project_list

#查询所有的功能菜单及其他系统相关的功能ID及功能名称
def funtionList():
    cursor = connection.cursor()
    SqlForFunction = "SELECT id,functionname FROM MySite_basefuntion WHERE description = '功能菜单' OR description = '其他系统'"

    cursor.execute(SqlForFunction)
    function_list = cursor.fetchall()

    return function_list

#查询某个角色所具备的角色
def funtion_List(roleid):
    cursor = connection.cursor()
    SqlForFunction = "SELECT aa.`id`,aa.`functionname`,CASE WHEN  bb.`role_id` IS NULL THEN 0 ELSE 1 END AS 'IsAllow' FROM MySite_basefuntion aa" \
                     " LEFT JOIN MySite_funtionrole bb" \
                     " ON aa.`id`=bb.`function_id`" \
                     " AND bb.`role_id`=%s " \
                     " ORDER BY aa.id ASC"%roleid

    cursor.execute(SqlForFunction)
    function_list = cursor.fetchall()

    return function_list

cursor.close()
connection.close()