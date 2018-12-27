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

    html = xml.Element("html")
    #body = xml.SubElement(html, "body", {"style":"background-color: #00e296;"})
    body = xml.SubElement(html, "body", {"style":"background-color: #00b336;"})

    xml.SubElement(body,"h1").text = "Report at "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    xml.SubElement(body,"h2").text = "Statistic:"
    for host in hosts:
        sessionList = backupSessionMap[host]
        success=0
        warning=0
        error=0
        if len(sessionList.List()) == 0:
            continue
        
        for sessionInfo in sessionList.List():
            if sessionInfo.State() == "Success":
                success +=1
            elif sessionInfo.State() == "Warning":
                warning +=1
            else:
                error +=1

        latestSessionInfo = sessionList.List()[-1]
        attr = {}
        if latestSessionInfo.State() == "Success":
            #attr["style"] = "background-color: #00b336;"
            attr["style"] = "background-color: #005f4b; color: white;"
        elif latestSessionInfo.State() == "Warning":
            attr["style"] = "background-color: #93ea20;"
        else:          
            attr["style"] = "background-color: #ba0200; color: white;"
                    
        xml.SubElement(xml.SubElement(body,"p"),"span", attr).text = \
            host + " - "+str(success)+"/"+str(warning)+"/"+str(error)+" Success/Warning/Error"

            
    for host in hosts:
        sessionList = backupSessionMap[host]
        
        xml.SubElement(body,"h2").text = host+":"

        tableStyle =xml.SubElement(body,"style")
        tableStyle.attrib["type"] = "text/css"
        tableStyle.text = "TABLE {border: 1px solid green;} TD{ border: 1px solid green; padding: 4px;}" 
        
        table = xml.SubElement(body,"table")
        thead = xml.SubElement(table, "thead")
        xml.SubElement(thead, "th").text = "Number"
        xml.SubElement(thead, "th").text = "State"
        xml.SubElement(thead, "th").text = "Job name"
        xml.SubElement(thead, "th").text = "Start at"
        xml.SubElement(thead, "th").text = "Complete at"
        
        tbody = xml.SubElement(table, "tbody")
        inx = 0
        for sessionInfo in reversed(sessionList.List()):
            if inx == 10:
                #xml.SubElement(body,"p").text = "..."
                break;
            tr = xml.SubElement(tbody,"tr")
            xml.SubElement(tr, "td").text = str(inx)

            attr ={}
            if sessionInfo.State() == "Success":
                pass
            elif sessionInfo.State() == "Warning":
                attr["style"] ="background-color: #93ea20;"
            else:  
                attr["style"] ="background-color: #ba0200; color: white;" 
            xml.SubElement(tr, "td", attr).text = sessionInfo.State()
            
            xml.SubElement(tr, "td").text = sessionInfo.JobName()
            xml.SubElement(tr, "td").text = sessionInfo.StartTime()
            xml.SubElement(tr, "td").text = sessionInfo.FinishTime()

            inx += 1

    xml.ElementTree(html).write("summary.html", encoding='utf-8', method='html')
    return 0

exit(main())
