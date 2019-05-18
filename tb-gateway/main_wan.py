# coding: UTF-8
import time

import Utils
from mqtt import tb_client
from mqtt import test_wan
import config.config as config


def onConnection():
    test_wan.start()


def onAttributeRespCallback(device, attributes):
    Utils.log(device)
    Utils.log(attributes)


def onAttributeUpdateCallback(device, attributes):
    Utils.log(device)
    Utils.log(attributes)


def onRpcCallback(device, method, params):
    Utils.log(device)
    Utils.log(method)
    Utils.log(params)

'''
    -host=MQTT服务器地址
    -port=MQTT端口号
    -token=链接TOKEN
    -mock=true 开启模拟数据
    -mock_period=发送数据间隔 单位:秒
    -mock_data=包含发送数据的文件
'''
if __name__ == '__main__':
    connect_config = config.configs.MQTT_CONNECT
    Utils.log(connect_config)

    if "host" not in connect_config or "port" not in connect_config or "token" not in connect_config:
        Utils.log("host,port,token not found", 'error')
        exit(-1)

    handler = {
        "onConnectionCallback": onConnection,
        "onAttributeRespCallback": onAttributeRespCallback,
        "onAttributeUpdateCallback": onAttributeUpdateCallback,
        "onRpcCallback": onRpcCallback
    }

    # 启动MQTT client
    tb_client.Connection(connect_config.host, connect_config.port, connect_config.token, handler)
    tb_client.start()

    while True:
        time.sleep(1000)

