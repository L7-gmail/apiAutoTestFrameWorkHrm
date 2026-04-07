import os
import shutil
import pytest

if __name__ == '__main__':
    pytest.main()
    shutil.copy('./environment.xml', './report/temp')
    # os.system('allure serve ./report/temp')
    os.system('allure generate ./report/temp -o ./report/html --clean')