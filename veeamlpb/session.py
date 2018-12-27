#!/usr/bin/python
# -*- coding: utf-8 -*-

from veeamlpb.subproccall import subproccall
from exceptions import ValueError

import xml.etree.ElementTree as xml


class CSession:
    @staticmethod
    def List():
        return subproccall( ["veeamconfig", "session", "list"] )

    @staticmethod
    def Stop(id):
        return subproccall( ["veeamconfig", "session", "stop", "--id", id] )

    @staticmethod
    def GetInfo(id):
        return subproccall( ["veeamconfig", "session", "info", "--id", id] )

class CSessionInfo(object):
    def __init__(self, id, type, jobName, state, startTime,finishTime):
        self.id = id
        self.type = type
        self.jobName = jobName;
        self.state = state;
        self.startTime = startTime;
        self.finishTime = finishTime

    def Id(self):
        return self.id

    def Type(self):
        return self.type

    def JobName(self):
        return self.jobName
    
    def State(self):
        return self.state

    def StartTime(self):
        return self.startTime

    def FinishTime(self):
        return self.finishTime        


    def ToString(self):
        return "id='" +self.id + "' type='" + self.type + "' jobName='"+self.jobName + "' state='" + self.state + "' startTime='" + self.startTime + "' finishTime='" + self.finishTime + "'"

    def ToXmlNode(self):
        root = xml.Element("sessionInfo")
        root.attrib["id"] = self.id
        root.attrib["type"] = self.type
        root.attrib["jobName"] = self.jobName
        root.attrib["state"] = self.state
        root.attrib["startTime"] = self.startTime
        root.attrib["finishTime"] = self.finishTime
        return root

    def ToXml(self):
        root = self.ToXmlNode()
        return  xml.tostring(root, 'utf-8')

    @staticmethod
    def FromXmlNode(root):
        id = root.attrib["id"]
        type = root.attrib["type"]
        jobName = root.attrib["jobName"]
        state = root.attrib["state"]
        startTime = root.attrib["startTime"]
        finishTime = root.attrib["finishTime"]

        return CSessionInfo(id, type, jobName, state, startTime, finishTime)

    @staticmethod
    def FromXml(string):
        root = xml.fromstring(string)
        return FromXmlNode(root)        

    @staticmethod
    def GetById(id):
        _state_raw = CSession.GetInfo(id)
        dataLines = []
        outlines = _state_raw.split('\n')
        for ln in outlines:
            lnstripped = ln.strip()
            if lnstripped.find(':') > 0:
                dataLines.append(lnstripped)

        id = ""
        type = ""
        jobName = ""
        state = ""
        startTime = ""
        finishTime = ""
        for dataline in dataLines:
            separatorPos = dataline.find(":")
            key = dataline[:separatorPos].strip()
            value = dataline[separatorPos+1:].strip()

            if key == "ID":
                id = value
            elif key == "Job name":
                jobName = value
            elif key == "State":
                state = value
            elif key == "Start time":
                startTime = value
            elif key == "End time":
                finishTime = value
            else:
                pass
        return CSessionInfo(id, type, jobName, state, startTime,finishTime)

class CSessionInfoList(object):
    def __init__(self, list):
        self.list = list

    def List(self):
        return self.list

    @staticmethod
    def Get():
        text = CSession.List()
        lines = text.split("\n")
        list = [] # session info list
        for line in lines:
            if len(line) == 0:
                continue

            words = line.split()
            if len(words) == 0:
                continue
            if words[0] == "Job":
                continue
            if words[0] == "Total":
                continue
            try:
                jobName = words[0]
                type = words[1]
                id = words[2]
                state = words[3]
                startTime = words[4] + " " + words[5]
                finishTime = words[6] + " " + words[7]
                list.append(CSessionInfo(id, type, jobName, state, startTime, finishTime))
            except:
                print "Failed to parse [", line, "]"
        return CSessionInfoList(list)

    def ToXmlNode(self):
        root = xml.Element("sessionInfoList")
        for sessionInfo in self.list:
            root.append(sessionInfo.ToXmlNode())
        return root

    def ToXml(self):
        root = self.ToXmlNode()
        return  xml.tostring(root, 'utf-8')

    @staticmethod
    def FromXmlNode(root):
        list = [] # session info list
        if root.tag != "sessionInfoList":
            raise RuntimeError("Invalid xml tag ["+root.tag+"]")
        for child in root:
            list.append(CSessionInfo.FromXmlNode(child))

        return CSessionInfoList(list)

    @staticmethod
    def FromXml(string):
        tree = xml.fromstring(string)
        return FromXmlNode(tree.getroot())

    @staticmethod
    def FromXmlFile(filename):
        sessionList = CSessionInfoList.FromXmlNode(xml.parse(filename).getroot())
        return sessionList

if __name__ == '__main__':
    pass