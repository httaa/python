# -*- conding:utf-8 -*-

""" 
@author: Salted fish 
@file: send.py
@time: 2019/01/16 
"""
import threading
import time
import logging
import schedule

import Utils
from config import config
from mqtt import tb_client
import modbus_tk.modbus_rtu as modbus_rtu
import serial
import modbus_tk.defines as cst
configs = config.configs

devices_status = {}
device_connection = tb_client.OnDeviceConnection
device_disconnection = tb_client.OnDeviceDisconnection


#PORT = "/dev/tty.usbserial-AL05HOBD"
PORT = "/dev/ttyUSB0"

master = ()

def mudebus_rtu_client():
    try:
        master = modbus_rtu.RtuMaster(
            serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0)
        )
        master.set_timeout(6)
        master.set_verbose(True)
    except BaseException:
        Utils.log('连接从机失败')
    return master

master = mudebus_rtu_client()

def send():
    Utils.log("send test start")
    ts = Utils.getTS()

    try:
        data_mod = Utils.readFile('/root/tb-gateway/config/test_data.json')

        data = master.execute(1, cst.READ_HOLDING_REGISTERS, 3, 3)
        Utils.log("data[] : {d}".format(d=data))
        Utils.log("data: w: {data}   w1:{data1}".format(data = data[0]/10,data1 = data[1]/10))
        data_mod = data_mod.replace("{time}", str(ts))
        data_mod = data_mod.replace("{ATC400}", str(data[0]/10))
        if data[1] == 65036 :
            data_mod = data_mod.replace("{ATE300}", str(0))
        else:
            data_mod = data_mod.replace("{ATE300}", str(data[1]/10))

        tb_client.SendTelemetry(data_mod, False)
        Utils.log("send test end")
    except Exception:
        logging.exception(" w send exception :")



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