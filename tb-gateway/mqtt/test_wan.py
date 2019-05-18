# -*- conding:utf-8 -*-
import threading
import time
import serial
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import schedule
import Utils
from mqtt import tb_client
from modbus import float_calculte as fc
import config.config as config

configs = config.configs

PORT = "/dev/ttyUSB0"

parms = ['Ua', 'Ub', 'Uc', 'Uab', ' Uca', 'Ubc', 'Ia', 'Ib', 'Ic', 'Pa',
         'Pb', 'Pc', 'P', 'Qa', 'Qb', 'Qc', 'Q', 'Sa', 'Sb', 'Sc', 'S',
         'PFa', 'PFb', 'PFc', 'PF', 'F', 'P_pos', 'Q_pos', 'P_rev', 'Q_rev']
# 发送数据格式
my_data = {
    "test":
        [
            {}
        ]
}


def modebus_rtu_client(port, baudrate=9600, timeout=6):
    try:
        master = modbus_rtu.RtuMaster(
            serial.Serial(port=port, baudrate=baudrate, bytesize=8, parity='N', stopbits=1, xonxoff=0)
        )
        master.set_timeout(timeout)
        master.set_verbose(True)
    except BaseException as e:
        Utils.log('端口 {} 不可用\n{}'.format(port, e), 'error')
        return
    Utils.log('连接从机成功')
    return master


master = modebus_rtu_client(PORT)


def send():
    # my_data = Utils.readJsonFile('config/test_data.json')
    values = {}
    try:
        data = master.execute(1, cst.READ_HOLDING_REGISTERS, 23, 58)
        if data:
            data = data.__iter__()

            for key in parms[:-3]:
                try:
                    values[key] = fc.pars(next(data), next(data))
                except ValueError:
                    values[key] = 0
            # 最后4个寄存器值
            last_data = list(data)
            try:
                values[parms[-3]] = fc.pars(last_data[0], last_data[1])
                values[parms[-2]] = fc.pars(last_data[1], last_data[2])
                values[parms[-1]] = fc.pars(last_data[2], last_data[3])
            except :
                pass
    except Exception as e:
        Utils.log('获取数据失败' + e.__str__(), 'error')

    if values:
        my_data['test'][0]['ts'] = Utils.getTS()
        my_data['test'][0]['values'] = values
        tb_client.SendTelemetry(my_data, True)
        Utils.log("数据推送")


def loop():
    while True:
        schedule.run_pending()
        time.sleep(1)


def start():
    # 开启定时上报
    schedule.every(configs.SEND_INTERVAL).seconds.do(send)
    # 开启新的线程
    t = threading.Thread(target=loop, name='send_data')
    t.setDaemon(True)
    t.start()
