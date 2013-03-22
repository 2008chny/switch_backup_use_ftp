#!/usr/bin/python2
#coding:utf-8


import sys
#import subprocess
from ftplib import *
sys.path.append('../src')
import tools
import switch_backup
from config import *


if __name__ == '__main__':
    print "Start FTP status check\n"
    print "    Try to connect to FTP Server,Please wait...\n"
    if tools.tcp_check(ftphost, ftpport) == "Failure":
        print "    Can't connect to FTP Server please check !\n"
        sys.exit(0)
    else:
        try:
            ftp = FTP(ftphost)
            ftp.connect(ftphost, ftpport, time_out)
            ftp.login(ftpuser, ftppass)
        except:
            print "    Can't login to FTP Server please check username and password!\n"
            sys.exit(0)
        else:
            print "    FTP Server Status OK \n"
            print "    Start create log forder\n"
            ftp = FTP(ftphost)
            ftp.connect(ftphost, ftpport, time_out)
            ftp.login(ftpuser, ftppass)
            data = ftp.nlst()
            if tools.str_check("log", data) is False:
                try:
                    ftp.mkd("log")
                except:
                    print "    Can't create log forder please check user perm!\n"
                    sys.exit(0)
                else:
                    print "    log forder has been created\n"
            else:
                    print "    log forder Already exists\n"

    for host in open("../conf/switch_list.csv"):
        if host:
            line_number, ip, tcpport, user, passwd, enpasswd, protocol, switch_type, other = host.split(",")
            print "    start check line " + line_number + "\n"
            if  tools.correct_ip(ip) is False:
                print "        " + ip + " are not correct ipaddress\n"
                logfile.write('    ip地址为:' + ip + '的交换机备份失败，IP地址不合法\n')
                print "        line " + line_number + " Error\n"
                continue

            try:
                tcpport = int(tcpport)
            except:
                print "        " + tcpport + " are not correct port\n"
                logfile.write('    ip地址为:' + ip + '的交换机备份失败，tcpport不合法\n')
                print "        line " + line_number + " Error\n"
                continue

            if  tcpport not in range(0, 65535):
                print "        " + tcpport + " are not correct port\n"
                logfile.write('    ip地址为:' + ip + '的交换机备份失败，tcpport不合法\n')
                print "        line " + line_number + " Error\n"
                continue

            if  tools.str_check(protocol, ('telnet', 'ssh')) is False:
                print "        protocol error\n"
                logfile.write('    ip地址为:' + ip + '的交换机备份失败，协议设置出错，目前只支持telnet及ssh\n')
                print "        line " + line_number + " Error\n"
                continue

            if  tools.str_check(switch_type, ('h3c', 'cisco')) is False:
                print "        switch_type error\n"
                logfile.write('    ip地址为:' + ip + '的交换机备份失败，设备类型设置出错，目前只支持h3c及cisco\n')
                print "        line " + line_number + " Error\n"
                continue

            print "        line " + line_number + " OK\n"

            print "    Start backup " + ip + " config file \n"
            if tools.tcp_check(ip, tcpport) == "Failure":
                print "    Can't connect to " + ip + " please check !\n"
                logfile.write('    ip地址为:' + ip + '的交换机连接超时，请核对IP地址是否正确\n')
            else:
                print "        Start create " + ip + " forder\n"
                data = ftp.nlst()
                if tools.str_check(ip, data) is False:
                    try:
                        ftp.mkd(ip)
                    except:
                        print "        Can't create " + ip + " forder please check user perm!\n"
                        sys.exit(0)
                    else:
                        print "        " + ip + " forder has been created\n"
                else:
                    print "        " + ip + " forder Already exists\n"

                if protocol == 'ssh':
                    switch_backup.ssh_cmd(ip, tcpport, user, passwd, enpasswd, switch_type)
                elif protocol == 'telnet':
                    switch_backup.telnet_cmd(ip, tcpport, user, passwd, enpasswd, switch_type)
            ftp = FTP(ftphost)
            ftp.connect(ftphost, ftpport, time_out)
            ftp.login(ftpuser, ftppass)
            data = ftp.nlst(ip)
            if  switch_type == "h3c":
                    backup_file = ip + "/startup.cfg." + now
            elif switch_type == "cisco":
                    backup_file = ip + "/" + ip + "-confg." + now
            if tools.str_check(backup_file, data) is True:
                print ('        ipaddress:' + ip + '  backup Successful\n')
                logfile.write('    ip地址为:' + ip + '的交换机备份成功\n')
            else:
                print ('        ipaddress:' + ip + '  backup Failure\n')
#                logfile.write('    ip地址为:'+ip+'的交换机备份失败\n')
#            subprocess.Popen('./diff.sh '+"/srv/ftp/xxxx/"+ip, shell=True)

    logfile.close()

    ftp = FTP(ftphost)
    ftp.connect(ftphost, ftpport, time_out)
    ftp.login(ftpuser, ftppass)
    #bufsize = 1024
    remotefilename = "交换机备份日志" + now + ".log"
    localfilename = "../log/交换机备份日志" + now + ".log"
    file_handler = open(localfilename, 'rb')
    #    ftp.mkd("log")
    time.sleep(2)
    ftp.cwd("log")
    time.sleep(1)
    ftp.storbinary("STOR " + remotefilename, file_handler)
    time.sleep(3)

    print "All Job done!"
