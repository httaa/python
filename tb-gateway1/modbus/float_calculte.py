# -*- coding: utf-8 -*-

"""
@Time : 2019-03-28 14:58
@Author : yangpeng
@File : float_calculte.py
"""

import math

def s(num1):
    if len(str(num1))==10:
        return 1
    else:
        return 0

def e(num1,num2):
    e = 0
    num1_list = get_list(num1)
    e_list = num1_list[1:len(num1_list)]
    if len(str(num2))==10:
        e_list.append(1)
    else:
        e_list.append(0)
    num = 128
    for s in e_list:
        e = e + int(s) * num
        num = num / 2

    return e


def get_list(num):
    num_list = list(bin(num))[2:len(list(bin(num)))]
    if len(list(str(num))) < 10:
        for i in range(10 - len(list(bin(num)))):
            num_list.insert(0, 0)

    return num_list

def x(num2, num3, num4):
    x = 1
    num2_list = get_list(num2)
    m_list = num2_list[1:len(num2_list)] + get_list(num3) + get_list(num4)
    i = 1
    for m in m_list:
        x = x + int(m) / math.pow(2,i)
        i = i + 1
    return x

def f(s,e,x):
    return math.pow(-1,s) * math.pow(2,e-127) * x


def get_data(num1,num2,num3,num4):
    return f(s(num1),e(num1,num2),x(num2,num3,num4))


def pars(s1,s2):
    s1 = '%x' % s1
    s2 = '%x' % s2
    num1 = int("".join(list(s1)[0:2]),16)
    num2 = int("".join(list(s1)[2:4]),16)
    num3 = int("".join(list(s2)[0:2]),16)
    num4 = int("".join(list(s2)[2:4]),16)

    return round(get_data(num1,num2,num3,num4),2)

if __name__ == '__main__':

    print(hex(17258))

    print('%x' % 17258)

    print(int('6a',16))

    s1 = '%x' % 17258
    print("".join(list(s1)[0:2]))
    print("".join(list(s1)[2:4]))


    print(pars(17258,59560))


