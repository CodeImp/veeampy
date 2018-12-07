#!/usr/bin/python
# -*- coding: utf-8 -*-

import veeamlpb
import os
import datetime
import xml.etree.ElementTree as xml

def main():

    hosts = []
    backupsDirectory = "/home/user/backups"
    for item in os.listdir(backupsDirectory):
        if item in [".", ".."]:
            continue
        if os.path.isdir(os.path.join(backupsDirectory,item)):
            hosts.append(item)
            print "item: ",item

    if len(hosts) == 0:
        return 0

    backupSessionMap = {}
    for host in hosts:
        print "found host: ", host
        sessionInfoFile = os.path.join(os.path.join(backupsDirectory,host), "session_list.xml")
        sessionList = veeamlpb.session.CSessionInfoList.FromXmlFile(sessionInfoFile)
        backupSessionMap[host] = sessionList

        for sessionInfo in sessionList.List():
            print "Session:",sessionInfo.ToString()

    #for host in hosts:
    html = xml.Element("html")
    body = xml.SubElement(html, "body")


    xml.SubElement(body,"p").text = ""

    xml.SubElement(body,"p").text = "Report at "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    xml.SubElement(body,"p").text = "Statistic:"
    for host in hosts:
        sessionList = backupSessionMap[host]
        success=0
        warning=0
        error=0
        for sessionInfo in sessionList.List():
            if sessionInfo.State() == "Success":
                success +=1
            elif sessionInfo.State() == "Warning":
                warning +=1
            else:
                error +=1

        xml.SubElement(body,"p").text = host + " - "+str(success)+"/"+str(warning)+"/"+str(error)+" Success/Warning/Error"
    xml.SubElement(body,"p").text = ""

    for host in hosts:
        sessionList = backupSessionMap[host]
        
        xml.SubElement(body,"p").text = "Last 10 session for host "+host
        inx = 0        
        for sessionInfo in reversed(sessionList.List()):
            if inx == 10:
                xml.SubElement(body,"p").text = "..."
                break;

            xml.SubElement(body,"p").text = str(inx)+" | "+sessionInfo.State()+" | "+sessionInfo.JobName()+" | "+sessionInfo.StartTime()+" / "+sessionInfo.FinishTime()
            inx += 1

    xml.ElementTree(html).write("summary.html", encoding='utf-8', method='html')
    return 0

exit(main())