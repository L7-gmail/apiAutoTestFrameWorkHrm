import configparser

from config.setting import FILE_PATH
from util_tools.log_util.RecordLog import logs


class ConfigParser:

    def __init__(self, filepath):
        self.config = configparser.ConfigParser()
        self.filepath = filepath
        self.read_config()

    def read_config(self):
        # 读配置文件
        try:
            self.config.read(self.filepath)
            logs.info(f"读取配置文件：{self.filepath}")
        except Exception as e:
            logs.error(f"读取配置文件，发送异常: {str(e)}")
            raise

    def get_value(self, section, option):
        """
        获取配置文件信息
        :param section: 要获取的信息所在区域
        :param option: 要获取的信息所在区域的字段值
        :return: 要获取的配置文件信息值
        """
        try:
            value = self.config.get(section, option)
            logs.info(f"获取配置文件的 {section} 下的 {option} 值: {value}")
            return value
        except Exception as e:
            logs.error(f"获取配置文件的 {section} 下的 {option} 值，发送异常: {str(e)}")
            raise

    def get_host(self):
        """
        获取项目host
        :return: 项目host
        """
        try:
            value = self.config.get('HOST', 'ecshop_host')
            logs.info(f"获取项目host:{value}")
            return value
        except Exception as e:
            logs.error(f"获取项目host，发送异常: {str(e)}")
            raise

    def get_section_mysql(self,option):
        """
        获取mysql配置信息
        :param option: 要获取的mysql 某配置信息
        :return:要获取的mysql 配置信息值
        """
        try:
            value = self.config.get('MYSQL', option)
            logs.info(f"获取mysql {option} ：{value}")
            return value
        except Exception as e:
            logs.error(f"获取mysql {option} ，发送异常: {str(e)}")
            raise


if __name__ == '__main__':
    configParser = ConfigParser(FILE_PATH.get("config_ini"))
    print(configParser.get_value('HOST', 'ecshop_host'))
    print(configParser.get_host())
    print(configParser.get_section_mysql("host"),configParser.get_section_mysql('port'),configParser.get_section_mysql('user'),\
          configParser.get_section_mysql('password'),configParser.get_section_mysql('database'),configParser.get_section_mysql('charset'))

