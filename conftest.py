import time

import pytest

from config.setting import IS_DINGDING_MSG
from util_tools.ConnectMysql import ConnectMysql
from util_tools.dingRebot import send_dd_msg
from util_tools.log_util.RecordLog import logs


@pytest.fixture(scope='session', autouse=True)
def delete_mysql_test_data():
    connect_mysql = ConnectMysql()
    goods_name = '纸巾-test'
    goods_inventory = 10
    shop_price = 12.5
    insert_good_sql = f"""
                        INSERT INTO `ecshop`.`ecs_goods` VALUES (null, 2, 'SJ03', 
                        '{goods_name}', '+', 18, 2, '', {goods_inventory}, 0.000, 24.00, {shop_price}, 0.00, 0, 0, 1, '', 
                        '', '', 'images/202603/thumb_img/3_thumb_G_1772682910673.jpg', 
                        'images/202603/goods_img/3_G_1772682910801.jpg', 
                        'images/202603/source_img/3_G_1772682910488.jpg', 1, '', 1, 1, 0, 0, 1771596948, 100, 0, 1, 
                        1, 1, 0, 0, 1772683459, 0, '', -1, -1, 0, NULL)
                    """
    connect_mysql.upd_del_add(insert_good_sql, close_connect=False)  # 创造测试数据-商品

    insert_user_address_sql = """
    INSERT INTO `ecshop`.`ecs_user_address` VALUES (null, '', 64, 'admin131415', 'test03@163.com', 1, 6, 77, 705, 'A小区',
     '12345', '1234567890', '18307875933', '', ''),(null, '', 64, 'test03', 'test03@163.com', 1, 6, 76, 696, 'B小区', 
     '123456', '1234567890', '18307875933', '', '');
    """
    connect_mysql.upd_del_add(insert_user_address_sql, close_connect=False)  # 创造测试数据-用户地址

    insert_user_sql = """
    INSERT INTO `ecshop`.`ecs_users` VALUES (null, 'test01@163.com', 'test01', 'e10adc3949ba59abbe56e057f20f883e', '', 
    '', 0, '0000-00-00', 0.00, 0.00, 0, 0, 0, 1772770305, 1772770305, '0000-00-00 00:00:00', '0.0.0.0', 1, 0, 0, NULL, 
    '0', 0, 0, '', 'test01@163.com', '1669931272', '12345678901', '13800138006', '13807875933', 0, 0.00, 'old_address', 
    '广州');
    """
    connect_mysql.upd_del_add(insert_user_sql, close_connect=False)  # 创造测试数据-新用户

    yield
    logs.info("正在清理(更新)数据库测试数据")
    delete_user_sql = """
    delete from ecs_users where email in ('L77@qq.com','L1234@qq.com','test01@163.com') and user_name in ('L77','L1234',
    'test01')
    """
    delete_good_sql = "delete from ecs_goods where goods_name = '纸巾-test' and goods_sn='SJ03' "
    delete_user_address_sql = "delete from ecs_user_address where email = 'test03@163.com' "
    connect_mysql.upd_del_add(delete_user_sql, close_connect=False)  # 删除测试数据-测试用户
    connect_mysql.upd_del_add(delete_user_address_sql, close_connect=False)  # 删除测试数据-用户地址
    connect_mysql.upd_del_add(delete_good_sql, close_connect=True)  # 删除测试数据-商品


# 全局变量存储测试开始时间
_test_start_time = None


def pytest_sessionstart(session):
    """测试会话开始时记录时间"""
    global _test_start_time
    _test_start_time = time.time()


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """pytest预定义的钩子函数，用于自动收集测试结果"""
    global _test_start_time

    total = terminalreporter._numcollected
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    error = len(terminalreporter.stats.get('error', []))
    skipped = len(terminalreporter.stats.get('skipped', []))

    # 计算执行时长
    if _test_start_time:
        duration = round(time.time() - _test_start_time, 2)
    else:
        duration = "N/A"

    summary = f"""
    自动化测试结果，通知如下，具体执行结果如下：
    测试用例总数：{total}
    测试通过数：{passed}
    测试失败数：{failed}
    错误数量：{error}
    跳过执行数量：{skipped}
    执行总时长：{duration}s
    """
    if IS_DINGDING_MSG:
        send_dd_msg(summary)
