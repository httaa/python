# -*- conding:utf-8 -*-

""" 
@author: Salted fish 
@file: data.py
@time: 2019/01/12 
"""

import config.config as config
import modbus.modbus as modbus

protocol_address = config.configs.MODBUS_PROTOCOL_ADDRESS
"""
遥测数据相关配置
"""
TELEMETRY_START_ADDRESS = protocol_address.telemetry_start_address  # 遥测数据报文开始地址
TELEMETRY_END_ADDRESS = protocol_address.telemetry_end_address  # 遥测数据报文结束地址
GET_TELEMETRY_STEP = protocol_address.get_telemetry_step  # 遥测数据获取数据步长

"""
遥信数据相关配置
"""
TELECOMMAND_START_ADDRESS = protocol_address.telecommand_start_address  # 遥信数据报文开始地址
TELECOMMAND_END_ADDRESS = protocol_address.telecommand_end_address  # 遥信数据报文结束地址
GET_TELECOMMAND_STEP = protocol_address.get_telecommand_step  # 遥信数据获取数据步长

"""
电度数据相关配置
"""
ELECTRICAL_START_ADDRESS = protocol_address.electrical_start_address  # 电度数据报文开始地址
ELECTRICAL_END_ADDRESS = protocol_address.electrical_end_address  # 电度数据报文结束地址
GET_ELECTRICAL_STEP = protocol_address.get_electrical_step  # 电度数据获取数据步长

"""
寄存器类型
"""
HOLDING_REGISTERS_TYPE = 40001  # 保持寄存器
DISCRETE_INPUTS_TYPE = 10001  # 离散输入寄存器


def get_data(start_address, end_address, func, type, step):
    """
    获取modbusTCP数据
    :param start_address:   报文开始地址
    :param end_address:     报文结束地址
    :param func:            获取数据方法
    :param type:            寄存器类型
    :param step:            步数(每次获取数据量 最大125)
    :return:                dict 遥测数据
    """
    data = ()
    num = step
    for i in range(start_address, end_address, step):
        if i + num >= end_address:
            num = end_address - i
        data += func(i, num)

    list1 = list(data)
    list2 = [i for i in range(start_address + type, end_address + type)]
    return dict(zip(list2, list1))


def get_telemetry_data():
    """
    获取遥测数据
    :return: dict 遥测数据
    """
    func = modbus.get_keep_data
    return get_data(TELEMETRY_START_ADDRESS, TELEMETRY_END_ADDRESS, func, HOLDING_REGISTERS_TYPE, GET_TELEMETRY_STEP)


def get_telecommand_data():
    """
    获取遥信数据
    :return: dict 遥信数据
    """
    func = modbus.get_digital_data
    return get_data(TELECOMMAND_START_ADDRESS, TELECOMMAND_END_ADDRESS, func, DISCRETE_INPUTS_TYPE,
                    GET_TELECOMMAND_STEP)


def get_electrical_data():
    """
    获取电度数据
    :return: dict 电度数据
    """
    func = modbus.get_keep_data
    return get_data(ELECTRICAL_START_ADDRESS, ELECTRICAL_END_ADDRESS, func, HOLDING_REGISTERS_TYPE,
                    GET_ELECTRICAL_STEP)


def get_devices_data():
    """
    获取设备所有数据
    :return:
    """
    # 获取遥测数据
    telemetry_data = get_telemetry_data()
    # 获取电度数据
    electrical_data = get_electrical_data()
    # 获取遥信数据
    telecommand_data = get_telecommand_data()
    # 合并数据
    devices_data = {}
    devices_data.update(telemetry_data)
    devices_data.update(electrical_data)
    devices_data.update(telecommand_data)
    return devices_data
