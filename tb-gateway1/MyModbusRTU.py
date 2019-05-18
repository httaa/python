# -*- conding:utf-8 -*-

import serial
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import schedule
import time
import threading
import Utils
import config.config as config
import traceback
from mqtt import tb_client

configs = config.configs
connect_config = configs.MODBUS_SLAVE_CONNECT

#PORT = "/dev/tty.usbserial-AL05HNOO"
#PORT = "/dev/tty.usbserial-1410"
#PORT = "/dev/tty.usbserial-AL05HNQW"
PORT  = "/dev/ttyUSB1"
PORT1 = "/dev/ttyUSB0"
PORT2 = "/dev/ttyUSB2"

master = ()
master1 = ()
master2 = ()

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

#HZ
def mudebus_rtu_client1():
    try:
        master = modbus_rtu.RtuMaster(
            serial.Serial(port=PORT1, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0)
        )
        master.set_timeout(6)
        master.set_verbose(True)
    except BaseException:
        Utils.log('连接从机失败')
    return master

master1 = mudebus_rtu_client1()

#W1
def mudebus_rtu_client2():
    try:
        master = modbus_rtu.RtuMaster(
            serial.Serial(port=PORT2, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0)
        )
        master.set_timeout(6)
        master.set_verbose(True)
    except BaseException:
        Utils.log('连接从机失败')
    return master

master2 = mudebus_rtu_client2()

def send():
    data = ()
    try:
        #data2 = master.execute(2, cst.READ_HOLDING_REGISTERS, 0, 2)
        data = master.execute(1, cst.WRITE_SINGLE_COIL, 0, 2)
        Utils.log('')
        Utils.log('获取温湿度数据 data1 {data}'.format(data = data))
        #Utils.log('获取温湿度数据 data2 {data}'.format(data=data2))
        Utils.log('')

        data_mod = Utils.readJsonFileFile('config/th_data.json')
        data_mod = data_mod.replace("{time}",str(Utils.getTS()))
        data_mod = data_mod.replace("{h}", str(data[0]/10))
        data_mod = data_mod.replace("{t}", str(data[1]/10))
    except BaseException:
        Utils.log('温湿度获取失败','error')

    if data:
        tb_client.SendTelemetry(data_mod,False)
        Utils.log("数据推送 '湿度'：{humidity}，‘温度’:{temperature} ".format(humidity = data[0]/10, temperature = data[1]/10))

def send2():
    try:
        data = master.execute(5, 4, 0, 6)
        data2 = master.execute(5, 1, 0, 6)
        Utils.log('')
        Utils.log('send2 data {data}'.format(data = data))
        Utils.log('')

        data_mod = Utils.readJsonFile('config/wd_data.json')

        data_mod = data_mod.replace("{time}", str(Utils.getTS()))
        data_mod = data_mod.replace("{1A}", str(data[0]))
        data_mod = data_mod.replace("{1B}", str(data[1]))
        data_mod = data_mod.replace("{1C}", str(data[2]))
        data_mod = data_mod.replace("{2A}", str(data[3]))
        data_mod = data_mod.replace("{2B}", str(data[4]))
        data_mod = data_mod.replace("{2C}", str(data[5]))

        data_mod = data_mod.replace("{1A_p}", str(data2[0]))
        data_mod = data_mod.replace("{1B_p}", str(data2[1]))
        data_mod = data_mod.replace("{1C_p}", str(data2[2]))
        data_mod = data_mod.replace("{2A_p}", str(data2[3]))
        data_mod = data_mod.replace("{2B_p}", str(data2[4]))
        data_mod = data_mod.replace("{2C_p}", str(data2[5]))

        #Utils.log('data2 JSON: {data}'.format(data = data_mod))
        if data:
            tb_client.SendTelemetry(data_mod, False)
            Utils.log('send success')
    except BaseException as e:
        Utils.log('get error','error')
        Utils.log('except:{s}'.format(s = str(e)))
        Utils.log('traceback.print_exc():{s}'.format(s = str(traceback.print_exc())))



def send3():
    try:
        data = master.execute(8, 3, 0, 7)
        # Utils.log('')
        Utils.log('data3 {data}'.format(data = data))
        # Utils.log('')
        # data_mod = Utils.readFile('config/test_data.json')
        # data_mod = data_mod.replace("{time}", str(Utils.getTS()))
        # Utils.log(data_mod)
        # if data_mod:
        #     tb_client.SendTelemetry(data_mod, False)
        #     Utils.log('send success')
    except BaseException as e:
        Utils.log('get error','error')
        Utils.log('except:{s}'.format(s=str(e)))
        Utils.log('traceback.print_exc():{s}'.format(s=str(traceback.print_exc())))


def send_frt():
    try:

        CT_Var_AH10 = 30
        PT_Var_AH10 = 100
        CT_Var_1D5_8 = 80
        PT_Var_1D5_8 = 1
        CT_Var_5D3_2 = 30
        PT_Var_5D3_2 = 1

        time = Utils.getTS()
        #AH10
        data = master.execute(4, 3, 0, 15)
        Utils.log('data_frt_AH10 {data}'.format(data=data))
        #1D5-8
        data1 = master.execute(2, 3, 0, 15)
        Utils.log('data_frt_1D5-8 {data}'.format(data=data1))
        #HZ-GZDW
        data2 = master1.execute(1, 3, 0, 7)
        Utils.log('data_frt_HZ-GZDW {data}'.format(data=data2))
        #W1 C
        data3 = master2.execute(5, 4, 0, 6)
        Utils.log('data_frt_W1 C {data}'.format(data=data3))
        #W1 D
        data4 = master2.execute(5, 1, 0, 6)
        Utils.log('data_frt_W1 D {data}'.format(data=data4))
        # 5D3-2
        data5 = master.execute(3, 3, 0, 15)
        Utils.log('data_frt_5D3-2 {data}'.format(data=data5))

        data_mod = Utils.readFile('config/frt_data.json')
        data_mod = data_mod.replace("{AH10_time}", str(time))
        data_mod = data_mod.replace("{AH10_Ua}",   str(data[0]/10 * PT_Var_AH10))
        data_mod = data_mod.replace("{AH10_Ub}",   str(data[1]/10 * PT_Var_AH10))
        data_mod = data_mod.replace("{AH10_Uc}",   str(data[2]/10 * PT_Var_AH10))
        data_mod = data_mod.replace("{AH10_Ia}",   str( '%.3f' % (data[3]/1000 * CT_Var_AH10) ))
        data_mod = data_mod.replace("{AH10_Ib}",   str( '%.3f' % (data[4]/1000 * CT_Var_AH10) ))
        data_mod = data_mod.replace("{AH10_Ic}",   str( '%.3f' % (data[5]/1000 * CT_Var_AH10) ))
        data_mod = data_mod.replace("{AH10_P}",    str( '%.3f' % (data[6]/1000 * PT_Var_AH10 * CT_Var_AH10) ))
        data_mod = data_mod.replace("{AH10_Q}",    str( '%.3f' % (data[7]/1000 * PT_Var_AH10 * CT_Var_AH10) ))
        data_mod = data_mod.replace("{AH10_S}",    str( '%.3f' % (data[8]/1000 * PT_Var_AH10 * CT_Var_AH10) ))
        data_mod = data_mod.replace("{AH10_F}",    str(data[9]/100))
        data_mod = data_mod.replace("{AH10_Pf}",   str(data[10]/10))
        data_mod = data_mod.replace("{AH10_Wh}",   str( '%.3f' % ( wvar(data[11],data[12]) /1000 * PT_Var_AH10 * CT_Var_AH10) ))
        data_mod = data_mod.replace("{AH10_Varh}", str( '%.3f' % ( wvar(data[13],data[14]) /1000 * PT_Var_AH10 * CT_Var_AH10) ))

        data_mod = data_mod.replace("{1D5-8_time}", str(time))
        data_mod = data_mod.replace("{1D5-8_Ua}",   str(data1[0] / 10 * PT_Var_1D5_8))
        data_mod = data_mod.replace("{1D5-8_Ub}",   str(data1[1] / 10 * PT_Var_1D5_8))
        data_mod = data_mod.replace("{1D5-8_Uc}",   str(data1[2] / 10 * PT_Var_1D5_8))
        data_mod = data_mod.replace("{1D5-8_Ia}",   str( '%.3f' % (data1[3] / 1000 * CT_Var_1D5_8) ))
        data_mod = data_mod.replace("{1D5-8_Ib}",   str( '%.3f' % (data1[4] / 1000 * CT_Var_1D5_8) ))
        data_mod = data_mod.replace("{1D5-8_Ic}",   str( '%.3f' % (data1[5] / 1000 * CT_Var_1D5_8) ))
        data_mod = data_mod.replace("{1D5-8_P}",    str( '%.3f' % (data1[6] / 1000 * PT_Var_1D5_8 * CT_Var_1D5_8) ))
        data_mod = data_mod.replace("{1D5-8_Q}",    str( '%.3f' % (data1[7] / 1000 * PT_Var_1D5_8 * CT_Var_1D5_8) ))
        data_mod = data_mod.replace("{1D5-8_S}",    str( '%.3f' % (data1[8] / 1000 * PT_Var_1D5_8 * CT_Var_1D5_8) ))
        data_mod = data_mod.replace("{1D5-8_F}",    str(data1[9] / 100))
        data_mod = data_mod.replace("{1D5-8_Pf}",   str(data1[10] / 10))
        data_mod = data_mod.replace("{1D5-8_Wh}",   str( '%.3f' % ( wvar(data[11],data[12]) / 1000 * PT_Var_1D5_8 * CT_Var_1D5_8) ))
        data_mod = data_mod.replace("{1D5-8_Varh}", str( '%.3f' % ( wvar(data[13],data[14]) / 1000 * PT_Var_1D5_8 * CT_Var_1D5_8) ))

        data_mod = data_mod.replace("{HZ-GZDW_time}",   str(time))
        data_mod = data_mod.replace("{HZ-GZDW_Ua}",     str(data2[0] / 10))
        data_mod = data_mod.replace("{HZ-GZDW_Ub}",     str(data2[1] / 10))
        data_mod = data_mod.replace("{HZ-GZDW_Uc}",     str(data2[2] / 10))
        data_mod = data_mod.replace("{HZ-GZDW_Uhm}",    str(data2[3] / 10))
        data_mod = data_mod.replace("{HZ-GZDW_Ukm}",    str(data2[4] / 10))
        data_mod = data_mod.replace("{HZ-GZDW_Idc}",    str(data2[5] / 10))
        data_mod = data_mod.replace("{HZ-GZDW_Ikm}",    str(data2[6] / 10))

        data_mod = data_mod.replace("{W1_time}", str(time))
        data_mod = data_mod.replace("{1A}",      str(data3[0]))
        data_mod = data_mod.replace("{1B}",      str(data3[1]))
        data_mod = data_mod.replace("{1C}",      str(data3[2]))
        data_mod = data_mod.replace("{2A}",      str(data3[3]))
        data_mod = data_mod.replace("{2B}",      str(data3[4]))
        data_mod = data_mod.replace("{2C}",      str(data3[5]))

        data_mod = data_mod.replace("{1A_p}",    str(data4[0]))
        data_mod = data_mod.replace("{1B_p}",    str(data4[1]))
        data_mod = data_mod.replace("{1C_p}",    str(data4[2]))
        data_mod = data_mod.replace("{2A_p}",    str(data4[3]))
        data_mod = data_mod.replace("{2B_p}",    str(data4[4]))
        data_mod = data_mod.replace("{2C_p}",    str(data4[5]))

        data_mod = data_mod.replace("{5D3-2_time}", str(time))
        data_mod = data_mod.replace("{5D3-2_Ua}",   str(data5[0] / 10 * PT_Var_5D3_2))
        data_mod = data_mod.replace("{5D3-2_Ub}",   str(data5[1] / 10 * PT_Var_5D3_2))
        data_mod = data_mod.replace("{5D3-2_Uc}",   str(data5[2] / 10 * PT_Var_5D3_2))
        data_mod = data_mod.replace("{5D3-2_Ia}",   str( '%.3f' % (data5[3] / 1000 * CT_Var_5D3_2) ))
        data_mod = data_mod.replace("{5D3-2_Ib}",   str( '%.3f' % (data5[4] / 1000 * CT_Var_5D3_2) ))
        data_mod = data_mod.replace("{5D3-2_Ic}",   str( '%.3f' % (data5[5] / 1000 * CT_Var_5D3_2) ))
        data_mod = data_mod.replace("{5D3-2_P}",    str( '%.3f' % (data5[6] / 1000 * PT_Var_5D3_2 * CT_Var_5D3_2) ))
        data_mod = data_mod.replace("{5D3-2_Q}",    str( '%.3f' % (data5[7] / 1000 * PT_Var_5D3_2 * CT_Var_5D3_2) ))
        data_mod = data_mod.replace("{5D3-2_S}",    str( '%.3f' % (data5[8] / 1000 * PT_Var_5D3_2 * CT_Var_5D3_2) ))
        data_mod = data_mod.replace("{5D3-2_F}",    str(data5[9] / 100))
        data_mod = data_mod.replace("{5D3-2_Pf}",   str(data5[10] / 10))
        data_mod = data_mod.replace("{5D3-2_Wh}",   str( '%.3f' % ( wvar(data[11],data[12]) / 1000 * PT_Var_5D3_2 * CT_Var_5D3_2) ))
        data_mod = data_mod.replace("{5D3-2_Varh}", str( '%.3f' % ( wvar(data[13],data[14]) / 1000 * PT_Var_5D3_2 * CT_Var_5D3_2) ))

        Utils.log(data_mod)
        if data_mod:
            tb_client.SendTelemetry(data_mod, False)
            Utils.log('send success')
    except BaseException as e:
        Utils.log('get error','error')
        Utils.log('except:{s}'.format(s=str(e)))
        Utils.log('traceback.print_exc():{s}'.format(s=str(traceback.print_exc())))

def wvar(num_before, num_after):
    num1 = '%x' % num_before
    num2 = '%x' % num_after
    str = num1 + num2
    num = int(str, 16)
    return num

def loop():
    while True:
        schedule.run_pending()
        time.sleep(1)



def start():
    # 初始化发送,通知系统设备连接成功
    #init_send()
    # 开启定时上报
    schedule.every(2).seconds.do(send_frt)
    # 开启新的线程
    t = threading.Thread(target = loop, name = 'send_ht_data')
    t.setDaemon(True)
    t.start()


if __name__ == "__main__":
    while True:

        send3()

        time.sleep(2)


