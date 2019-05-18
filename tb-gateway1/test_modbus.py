# -*- conding:utf-8 -*-

import serial
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import time
import Utils
import config.config as config
from modbus import float_calculte as fc

configs = config.configs
connect_config = configs.MODBUS_SLAVE_CONNECT

#PORT = "/dev/tty.usbserial-AL05HNOO"
#PORT = "/dev/tty.usbserial-1410"
#PORT = "/dev/tty.usbserial-AL05HNQW"
#PORT =  "/dev/ttyUSB0"
PORT = "/dev/tty.usbserial-AL05HOBD"
#PORT1 = "/dev/ttyUSB1"
#PORT2 = "/dev/ttyUSB2"

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

#OEM多功能仪表浮点计算
def send():
    try:
        data = master.execute(1, cst.READ_HOLDING_REGISTERS, 23, 2)

        num = fc.pars(data[0],data[1])

        Utils.log('')
        Utils.log('data: {data}'.format(data = data))
        Utils.log('num: {num}'.format(num=num))

        data2 = master.execute(1, cst.READ_HOLDING_REGISTERS, 73, 2)

        num2 = fc.pars(data2[0], data2[1])

        Utils.log('')
        Utils.log('data2: {data2}'.format(data2=data2))
        Utils.log('num2: {num2}'.format(num2=num2))
    except BaseException:
        Utils.log('获取失败','error')

def send2():
    try:
        data = master.execute(1, cst.READ_HOLDING_REGISTERS, 3, 2)

        Utils.log('')
        Utils.log('data: {data}'.format(data = data))

        Utils.log('')
    except BaseException:
        Utils.log('获取失败','error')


if __name__ == "__main__":
    while True:

        send2()

        time.sleep(2)


