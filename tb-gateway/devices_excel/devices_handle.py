# -*- conding:utf-8 -*-

""" 
@author: Salted fish 
@file: excel_handle.py 
@time: 2019/01/14 
"""
import xlrd
import json


def device_handel():
    devices = {}
    # 读取excel
    readbook = xlrd.open_workbook('devices_plan.xlsx')
    # 获取sheet
    sheet = readbook.sheet_by_name('设备参数')
    # 获取最大行
    max_row = sheet.nrows
    # 获取每行数据,组装数据格式
    for line in range(1, max_row):
        # 获取每行数据
        row = sheet.row_values(line)
        device_name = row[1]    # 设备名
        param = row[2]          # 参数名
        address = row[3]        # 寄存器地址
        # 组装设配数据结构
        if device_name in devices:
            device = devices[device_name]
        else:
            device = {}
        device["name"] = device_name
        device[param] = int(address)
        devices[device_name] = device
    devices_str = json.dumps(devices)
    # 写入设配配置文件
    file = open('../config/device_config_plan.json', 'w')
    file.write(devices_str)
    file.close()


if __name__ == '__main__':
    device_handel()
