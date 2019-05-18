# -*- conding:utf-8 -*-

""" 
@author: Salted fish 
@file: bash_config.py 
@time: 2019/01/17 
"""
import socket

hostname = socket.gethostname()
if hostname == 'lizhihuideMacBook-Pro.local':
    configs = {
        "PYTHON_PATH": "python3.6"
    }
else:
    configs = {
        "PYTHON_PATH": "/usr/bin/python3.5"
    }
