import serial
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import schedule
import time
import Utils
import config.config as config

configs = config.configs
connect_config = configs.MODBUS_SLAVE_CONNECT

#PORT = "/dev/tty.usbserial-AL05HNOO"
#PORT = "/dev/tty.usbserial-A601OCKE"
PORT = "/dev/ttyUSB0"

master = ()
def mudebus_rtu_client():
    try:
        master = modbus_rtu.RtuMaster(
            serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0)
        )
        master.set_timeout(3)
        master.set_verbose(True)
    except BaseException:
        Utils.log('连接从机失败')
    return master

master = mudebus_rtu_client()

def send():
    try:
        data = master.execute(101, cst.READ_HOLDING_REGISTERS,0, 20)
        data2 = master.execute(104, cst.READ_HOLDING_REGISTERS, 0, 20)
        Utils.log('')
        Utils.log('101 {data}'.format(data=data))
        Utils.log('104 {data}'.format(data=data2))
        Utils.log('')
    except BaseException:
        Utils.log('智能仪表获取A相电压失败 test error','error')


def loop():
    while True:
        schedule.run_pending()
        time.sleep(1)



# def start():
#     # 初始化发送,通知系统设备连接成功
#     #init_send()
#     # 开启定时上报
#     schedule.every(2).seconds.do(send)
#     # 开启新的线程
#     t = threading.Thread(target = loop, name = 'send_ht_data')
#     t.setDaemon(True)
#     t.start()


if __name__ == "__main__":
    while True:
        send()
        time.sleep(1)


