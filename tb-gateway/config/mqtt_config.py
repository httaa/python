# -*- conding:utf-8 -*-

""" 
@author: Salted fish 
@file: mqtt_config.py 
@time: 2019/01/15 
"""
import socket

hostname = socket.gethostname()
if hostname == 'lizhihuideMacBook-Pro.local':
    configs = {
        "MQTT_CONNECT": {
            "host": "127.0.0.1",
            "port": 1883,
            "token": "XCOA3yJdDe8O7hkQsXYy"
        },
        "SEND_INTERVAL": 5,
    }
elif hostname == 'yangpengdeMBP-2':
    configs = {
        "MQTT_CONNECT": {
            "host": "60.205.202.24",
            "port": 31883,
            "token": "x3t5ABldjjXpDW1ZmGNZ",
            "gatewayname": "yangpengMac1"
        },
        "SEND_INTERVAL": 5,
    }
elif hostname == 'fu_rui_te_raspberrypi_master':
    configs = {
        "MQTT_CONNECT": {
            "host": "60.205.202.24",
            "port": 31883,
            "token": "3lUnHsoG6vy76GXZmnUM",
            "gatewayname": "fu_rui_te"
        },
        "SEND_INTERVAL": 2,
    }
else:
    configs = {
        "MQTT_CONNECT": {
            "host": "60.205.202.24",
            "port": 31883,
            "token": "ooYKWsZZXuGqDWkRYCPZ",
            "gatewayname": "other"
        },
        "SEND_INTERVAL": 5,
    }
