#!/usr/bin/python2
#coding:utf-8
'''
Created on 2012-7-19

@author: DARK_LBP
'''

import time

now = time.strftime("%Y%m%d", time.localtime())
time_out = 10
ftphost = "192.168.x.x"
ftpport = "21"
ftpuser = "ftpuser"
ftppass = "ftppass"

logfile = open("../log/交换机备份日志" + now + ".log", 'w')
logfile.write(now + '交换机备份日志\n')
