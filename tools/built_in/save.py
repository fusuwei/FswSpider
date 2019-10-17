from tools import log
import traceback
import os
logger = log(__name__)


async def before_save(items, table_name, Mysql, save_loop, sql_error):
    try:
        while True:
            show_table_sql = "show tables"
            result = Mysql.diy_sql(show_table_sql)
            tables = [list(i.values())[0] for i in result]
            item = items.get()
            items.task_done()
            if item.table_name:
                table_name = item.table_name
            elif table_name:
                table_name = table_name
            else:
                logger.error("请配置table_name!")
                raise Exception()
            data = item.to_dict()
            if table_name not in tables:
                Mysql.create_table(table_name, data)
                logger.warning("未填写表名，默认建立以脚本名为表名的表或者没有表")
            method = item.method
            ret = await save(Mysql, data, method, table_name, save_loop)
            if ret:
                raise Exception(ret)
    except Exception as e:
        items.put(item)
        sql_error()
        traceback.print_exc()
        os._exit(1)


async def save(mysql, data, method, table_name, loop):
    """
    存储函数，负责吧爬下的数据存到mysql数据库中
    :return:
    """
    try:
        if method == "insql":
            await loop.run_in_executor(None, mysql.insql, table_name, data)
        elif method == "update":
            values = data["values"]
            conditions = data["conditions"]
            await loop.run_in_executor(None, mysql.update, table_name, values, conditions)
        elif method == "delete":
            await loop.run_in_executor(None, mysql.delete, table_name, data)
    except Exception as e:
        return e
