# -*- codeing = utf-8 -*-
# @Time :2021/5/13 20:59
# @Author : 刘念卿
# @File : kill.py
# @Software : PyCharm
import os

def kill(pid):

    # 本函数用于中止传入pid所对应的进程

    if os.name == 'nt':

        # Windows系统

        cmd = 'taskkill /pid ' + str(pid) + ' /f'

        try:

            os.system(cmd)

            print(pid, 'killed')

        except Exception as e:

            print(e)

    elif os.name == 'posix':

        # Linux系统

        cmd = 'kill ' + str(pid)

        try:

            os.system(cmd)

            print(pid, 'killed')

        except Exception as e:

            print(e)

    else:

        print('Undefined os.name')