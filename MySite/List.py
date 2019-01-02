from django.db import connection, transaction
from MySite import models,Sql

class List():
    cursor = connection.cursor()
    sql = Sql.SqlStatement()

   # cursor.execute(sql.SqlForFunction)
   # function_list = cursor.fetchall()

   # cursor.execute(sql.SqlForOtherSystem)
   # other_system_list = cursor.fetchall()

    cursor.execute(sql.SqlForRuiPengErpAndHis)
    RuiPengErpAndHis_list = cursor.fetchall()

    cursor.execute(sql.SqlForRuiPengMicroservice)
    RuiPengMicroservice_list = cursor.fetchall()

    cursor.execute(sql.SqlForRuiPengApp)
    RuiPengApp_list = cursor.fetchall()

    cursor.execute(sql.SqlForHost)
    host_list = cursor.fetchall()

    cursor.execute(sql.SqlForHostList)
    hostlist = cursor.fetchall()

    cursor.execute(sql.SqlForErpHost)
    erp_host_list = cursor.fetchall()

    cursor.execute(sql.SqlForMicroserviceHost)
    microservice_host_list = cursor.fetchall()

    cursor.execute(sql.SqlForErpOtherHost)
    erpother_host_list = cursor.fetchall()

    cursor.execute(sql.SqlForProject)
    project_list = cursor.fetchall()

    cursor.execute(sql.SqlForErpProject)
    erp_project_list = cursor.fetchall()

    cursor.execute(sql.SqlForMicroserviceProject)
    microservice_project_list = cursor.fetchall()

    cursor.execute(sql.SqlForErpOtheProject)
    erpother_project_list = cursor.fetchall()

    cursor.execute(sql.SqlForUser)
    user_list = cursor.fetchall()

    cursor.execute(sql.SqlForRole)
    role = cursor.fetchall()

    cursor.close()
    connection.close()
