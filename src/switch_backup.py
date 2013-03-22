#!/usr/bin/python2
#coding:utf-8
'''
Created on 2012-7-19

@author: zhuwz
'''

import paramiko
#import cmd
import telnetlib
#import tools
#from socket import *
#from config import *


def ssh_cmd(ip, tcpport, user, passwd, enpasswd, type):
    if type == 'h3c':
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, port=tcpport, username=user, password=passwd, timeout=time_out)
        except paramiko.AuthenticationException:
            print ('        Auth Failed! Please check your username and password!')
            logfile.write('    ip地址为:' + ip + '的交换机认证失败，请核对帐号及密码\n')
            return 259

        except socket.error:
            print ('        connent timeout,please check your ipaddress')
            logfile.write('    ip地址为:' + ip + '的交换机连接超时，请核对IP地址是否正确\n')
            return 261
        else:
            chan = ssh.invoke_shell()
            cmd = "put startup.cfg" + " " + "startup.cfg." + now + "\n"
            time.sleep(2)
            chan.send("ftp " + ftphost + "\n")
            time.sleep(1)
            chan.send(ftpuser + "\n")
            time.sleep(1)
            chan.send(ftppass + "\n")
            time.sleep(2)
            chan.send("cd " + ip + "\n")
            time.sleep(2)
            chan.send(cmd)
            time.sleep(10)
            chan.send("quit\n")
            ssh.close()
#   cisco备份
    elif type == 'cisco':
        try :
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, port=tcpport, username=user, password=passwd, timeout=time_out)
        except paramiko.AuthenticationException:
            print ('        Auth Failed! Please check your username and password!')
            logfile.write('    ip地址为:' + ip + '的交换机认证失败，请核对帐号及密码\n')
            return 259

        except socket.error:
            print ('        connent timeout,please check your ipaddress')
            logfile.write('    ip地址为:' + ip + '的交换机连接超时，请核对IP地址是否正确\n')
            return 261
        except :
            print ('        other error')
            logfile.write('    ip地址为:' + ip + '的交换机连接失败。错误不明\n')
            return None
        else:
            chan = ssh.invoke_shell()
            cmd = "copy running-config ftp://" + ftpuser + ":" + ftppass + "@" + ftphost + "/" + ip + "/" + ip + "-confg." + now + "\n"
            chan.send("en \n")
            time.sleep(1)
            data = chan.recv(99999)
            chan.send(enpasswd + "\n")
            str = "Password:"
            data = chan.recv(99999)
            if str in data:
                print ('        Enable Auth Failed! Please check your username and password!')
                logfile.write('    ip地址为:' + ip + '的交换机enable认证失败，请核对帐号及密码\n')
                return None
            time.sleep(1)
            chan.send(cmd)
            time.sleep(2)
            chan.send("\n")
            time.sleep(2)
            chan.send("\n")
            time.sleep(10)
            ssh.close()




def telnet_cmd(ip, tcpport, user, passwd, enpasswd, type):
    if type == 'h3c':
        try :
            t = telnetlib.Telnet()
            t.open(ip, tcpport, time_out)
        except socket.error:
            print ('        connent timeout,please check your ipaddress')
            logfile.write('    ip地址为:' + ip + '的交换机连接超时，请核对IP地址是否正确\n')
            return 261
        else:
            cmd1 = "cd " + ip + "\n"
            cmd2 = "put startup.cfg" + " " + "startup.cfg." + now + "\n"
            time.sleep(2)
            t.write(user + "\n")
            time.sleep(2)
            t.write(passwd + "\n")
            e_index, e_match, e_data = t.expect(['Login failed!', '>'], time_out)
            if e_index == 0:
                print ('        Auth Failed! Please check your username and password!')
#                print (e_data)
                logfile.write('    ip地址为:' + ip + '的交换机认证失败，请核对帐号及密码\n')
                return 259
            else:
                time.sleep(2)
                t.write("ftp " + ftphost + "\n")
                time.sleep(2)
                t.write(ftpuser + "\n")
                time.sleep(2)
                t.write(ftppass + "\n")


                ret = t.read_until('[ftp]', 5)
                t.write(cmd1)
                ret = t.read_until('[ftp]', 5)
                t.write(cmd2)
                ret = t.read_until('[ftp]', 5)
                t.write("quit\n")
            t.close()

    elif type == 'cisco':
        try:
            t = telnetlib.Telnet()
            t.open(ip, tcpport, time_out)
        except socket.error:
            print ('        connent timeout,please check your ipaddress')
            logfile.write('    ip地址为:' + ip + '的交换机连接超时，请核对IP地址是否正确\n')
            return 261
        else:
            cmd = "copy running-config ftp://" + ftpuser + ":" + ftppass + "@" + ftphost + "/" + ip + "/" + ip + "-confg." + now + "\n"
            time.sleep(2)
            t.write(user + "\n")
            time.sleep(2)
            t.write(passwd + "\n")
            e_index, e_match, e_data = t.expect(['Login invalid', '>'], time_out)
            if e_index == 0:
                print ('        Auth Failed! Please check your username and password!')
#                print (e_data)
                logfile.write('    ip地址为:' + ip + '的交换机认证失败，请核对帐号及密码\n')
                return 259
            else:
                t.write("en\n")
                t.read_until("Password:", 5)
                t.write(enpasswd + "\n")
                time.sleep(2)
                e_index, e_match, e_data = t.expect(['Password:', '#'], time_out)
                if e_index == 0:
                    print ('        Enable Auth Failed! Please check your username and password!')
                    print (e_data)
                    logfile.write('    ip地址为:' + ip + '的交换机enable认证失败，请核对帐号及密码\n')
                    return 259
                else:
                    ret = t.read_until('#', 5)
                    t.write(cmd)
                    ret = t.read_until(']?', 5)
                    t.write("\n")
                    ret = t.read_until(']?', 5)
                    t.write("\n")
                    ret = t.read_until('#', 5)
                    t.write("quit\n")
            t.close()
