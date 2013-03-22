#!/usr/bin/python2 
#coding:utf-8
'''
Created on 2012-7-19

@author: zhuwz
'''


from socket import *
from config import *

"""
检测TCP端口是否存活
"""
def tcp_check(ip,tcpport):
    s = socket(AF_INET, SOCK_STREAM)
    tcpport = int(tcpport)
    try:
        s.connect((ip, tcpport))    #connect to server on the port
        s.shutdown(2)                #disconnect
#        print "Success. Connected to " + ip + " on port: " + str(tcpport)
        return "Success"
    except:
#        print "Failure. Cannot connect to " + ip + " on port: " + str(tcpport)
        return "Failure"
    
        
def str_check(str,data):
    if str in data:
        return True
    else:
        return False
    
    
def correct_ip(ip):
    # Check if my IP address has 4 numbers separated by dots
    num=ip.split('.')
    if not len(num)==4:
        return False
    # Check each of the 4 numbers is between 0 and 255
    for n in num:
        try:
            if int(n) < 0 or int(n) > 255:
                return False
        except:
            return False
    return True




