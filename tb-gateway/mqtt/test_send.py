# -*- conding:utf-8 -*-

""" 
@author: Salted fish 
@file: send.py
@time: 2019/01/16 
"""
import threading
import time

import schedule

import Utils
from config import config
from mqtt import tb_client

configs = config.configs

devices_status = {}
device_connection = tb_client.OnDeviceConnection
device_disconnection = tb_client.OnDeviceDisconnection


def send():
    Utils.log("send test start")
    ts = Utils.getTS()
    data_mod = Utils.readFile('config/test_data.json')
    data_mod = data_mod.replace("{time}", str(ts))
    tb_client.SendTelemetry(data_mod, False)
    Utils.log("send test end")



def loop():
    while True:
        schedule.run_pending()
        time.sleep(1)


def start():
    # 初始化发送,通知系统设备连接成功
    #init_send()
    # 开启定时上报
    schedule.every(configs.SEND_INTERVAL).seconds.do(send)
    # 开启新的线程
    t = threading.Thread(target = loop, name = 'send_data')
    t.setDaemon(True)
    t.start()