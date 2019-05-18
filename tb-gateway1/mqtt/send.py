# -*- conding:utf-8 -*-

""" 
@author: Salted fish 
@file: send.py
@time: 2019/01/16 
"""
import json
import threading
import time

import schedule
import random

import Utils
from config import config
from modbus import data as modbus_data
from mqtt import tb_client

configs = config.configs

devices_status = {}
device_connection = tb_client.OnDeviceConnection
device_disconnection = tb_client.OnDeviceDisconnection


def init_send():
    """
    初始化设备状态
    :return:
    """
    # 获取设配配置
    Utils.log("init send")
    try:
        devices = Utils.readJsonFile('config/device_config.json')
        for name, device in devices.items():
            # 保存设备初始化状态
            # 参数地址排序
            del device['name']
            addr = sorted(device.values())
            if addr:
                devices_status[name] = {'address': addr[0], 'status_func': device_connection, 'failure_count': 0}
            # 发送初始化状态
            tb_client.OnDeviceConnection(name)
    except BaseException:
        Utils.log('init send failure', 'error')


def device_status(device_name, status_func):
    """
    设备状态
    :param device_name: 设备名
    :param status_func: 当前状态
    :return:
    """
    failure_count = devices_status[device_name]['failure_count']

    # 判断状态是否改变
    if status_func == devices_status[device_name]['status_func']:
        if status_func == device_connection and failure_count > 0:
            devices_status[device_name]['failure_count'] = 0
        return

    # 连接保持
    if status_func == device_connection:
        # 修改状态,发送消息
        devices_status[device_name]['status_func'] = status_func
        status_func(device_name)
        # 清空失败次数
        devices_status[device_name]['failure_count'] = 0
        Utils.log('{device_name} - modbusTcp重新连接'.format(device_name = device_name), 'info')

    # 连接断开
    elif status_func == device_disconnection:
        # 失败计数
        devices_status[device_name]['failure_count'] = failure_count + 1
        # 判断失败次数
        if failure_count >= configs.CONNECTION_FAILURE:
            # 修改状态,发送消息
            devices_status[device_name]['status_func'] = status_func
            status_func(device_name)
            Utils.log('{device_name} - modbusTcp连接断开'.format(device_name = device_name), 'error')


def send():
    """
    发送遥测数据
    :return: None
    """
    Utils.log("send start")
    # 获取设配配置
    devices = Utils.readJsonFile('config/device_config.json')
    # 获取设备数据
    devices_data = modbus_data.get_devices_data()
    # 迭代设备
    data = {}
    # 时间
    ts = Utils.getTS()
    for name, device in devices.items():
        devices_param = {}
        # 匹配设备参数
        for k, v in device.items():
            if isinstance(v, str):
                continue
            if v in devices_data:
                devices_param[k] = devices_data[v]

                if name=='1D1' or name=='3D1':
                    if '-' not in k and len(k) < 4:
                        Utils.log('***********   ***********   ***********  *********** {name}  {k}={v}'.format(name=name,k=k,v=devices_data[v]),'info')

        if devices_param:
            # 组装设备数据结构
            data[name] = [{'ts': ts, 'devic': name, 'values': devices_param}]
            status = device_connection
        else:
            status = device_disconnection
        # 维护设备状态
        device_status(name, status)
    if data:
        # mqtt发送数据
        tb_client.SendTelemetry(json.dumps(data), False)
    Utils.log("send end")

def send_plan():

    Utils.log("send plan start")
    # 获取设配配置
    devices = Utils.readJsonFile('config/device_config_plan.json')
    # 迭代设备
    data = {}
    # 时间
    ts = Utils.getTS()
    for name, device in devices.items():

        for k, v in device.items():
            if 'I' in k :
                device[k] = v + random.randint(-100,200)/10
            elif 'P' == k :
                device[k] = v + random.randint(-300, 500) / 10

        # 组装设备数据结构
        data[name] = [{'ts': ts, 'devic': name, 'values': device}]
        #status = device_connection
        # 维护设备状态
        #device_status(name, status)
    if data:
        # mqtt发送数据
        tb_client.SendTelemetry(json.dumps(data), False)

        data_mod = Utils.readFile('config/th_data.json')
        data_mod = data_mod.replace("{time}", str(Utils.getTS()))
        data_mod = data_mod.replace("{h}", str(234 / 10))
        data_mod = data_mod.replace("{t}", str(178 / 10))

        tb_client.SendTelemetry(data_mod, False)

    Utils.log("send plan end")

def start_plan():
    # 初始化发送,通知系统设备连接成功
    init_send()
    # 开启定时上报
    schedule.every(configs.SEND_INTERVAL).seconds.do(send_plan)
    # 开启新的线程
    t = threading.Thread(target = loop, name = 'send_data')
    t.setDaemon(True)
    t.start()

def loop():
    while True:
        schedule.run_pending()
        time.sleep(1)


def start():
    # 初始化发送,通知系统设备连接成功
    init_send()
    # 开启定时上报
    schedule.every(configs.SEND_INTERVAL).seconds.do(send)
    # 开启新的线程
    t = threading.Thread(target = loop, name = 'send_data')
    t.setDaemon(True)
    t.start()
