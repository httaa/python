# -*- conding:utf-8 -*-

""" 
@author: yangpeng
@file: tb-gateway_test.py
@time: 2019/03/11
"""
import subprocess
import argparse
import Utils

import os
from config import config

configs = config.configs

baseDir = os.path.dirname(os.path.abspath(__file__))
main_path = os.path.join(baseDir, "main_test.py")
runtime_log_path = os.path.join(baseDir, 'runtime/logs/output/output.log')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help = "value:start, stop")
    parser.add_argument('-logs', help = 'runtime log, value:(int)line', type = int)
    args = parser.parse_args()

    if args.s == 'start':
        subprocess.Popen('nohup '+configs.PYTHON_PATH+' '+main_path+' >/dev/null 2>&1 &', shell = True)
        #Utils.log('-----程序开始运行-----')
        Utils.log('-----start-----')
    elif args.s == 'stop':
        pid = subprocess.check_output("ps aux | grep -v grep |grep 'tb-gateway/main_test.py' | awk '{print $2}'", shell = True)
        pid = str(pid[:-1], encoding = 'utf-8')
        if pid == '':
            #Utils.log('-----程序未运行-----')
            Utils.log('-----not start-----')
        else:
            subprocess.check_call(['kill', pid])
            #Utils.log("停止运行程序")
            Utils.log('----- stop -----')
    else:
        #Utils.log("请填写正确的指令,-h查看帮助")
        Utils.log("Please fill in the correct instruction,-h view the help")

    if args.logs:
        subprocess.check_call(['tail', '-f', '-n', str(args.logs), runtime_log_path])