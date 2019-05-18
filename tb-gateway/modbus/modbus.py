# -*- conding:utf-8 -*-

""" 
@author: Salted fish 
@file: modbus.py 
@time: 2019/01/12 
"""
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import config.config as config
import Utils

"""
获取配置文件
"""
configs = config.configs
connect_config = configs.MODBUS_SLAVE_CONNECT


def modbus_client():
    """
    连接从机
    :return:
    """
    # 连接从机地址
    try:
        client = modbus_tcp.TcpMaster(connect_config.host, connect_config.port, configs.CONNECTION_TIMEOUT)
    except BaseException:
        Utils.log('连接从机失败 - ip:{ip},port:{port}'.format(ip = connect_config.host, port = connect_config.port), 'error')
    return client


client = modbus_client()

def get_keep_data(start_address, num):
    """
    保持寄存器数据
    :param start_address:   报文开始地址git
    :param num:             寄存器数量
    :return:                tuple
    """
    keep_data = ()
    Utils.log('获取保持寄存器数据 - 开始地址:{addr},寄存器数量:{num}'.format(addr = start_address, num = num))
    try:
        keep_data = client.execute(connect_config.slave_id, cst.READ_HOLDING_REGISTERS, start_address, num)
    except BaseException:
        Utils.log('modbusTCP获取保持寄存器数据失败 - 开始地址:{addr},寄存器数量:{num}'.format(addr = start_address, num = num), 'error')
    return keep_data


def get_digital_data(start_address, num):
    """
    数字量输入寄存器数据
    :param start_address:   报文开始地址
    :param num:             寄存器数量
    :return:                tuple
    """
    digital_data = ()
    Utils.log('获取数字量输入寄存器数据 - 开始地址:{addr},寄存器数量:{num}'.format(addr = start_address, num = num))
    try:
        digital_data = client.execute(connect_config.slave_id, cst.READ_DISCRETE_INPUTS, start_address, num)
    except BaseException:
        Utils.log('modbusTCP获取离散寄存器数据失败 - 开始地址:{addr},寄存器数量:{num}'.format(addr = start_address, num = num), 'error')
    return digital_data
