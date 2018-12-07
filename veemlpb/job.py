#!/usr/bin/python
# -*- coding: utf-8 -*-

from subproccall import *
from veeamlpb import session
import xml.etree.ElementTree as xml

class CJob:
    @staticmethod
    def NewVolumeBackup(jobName, repoName, devices):
        ''' devices - is a comma separated name of devices or mount points or ...'''
        return subproccall( ["veeamconfig", "job", "create", "--name", jobName, "--repoName", repoName, "--objects", devices] )

    @staticmethod
    def NewFileBackup(jobName, repoName, includeDirs):
        return subproccall( ["veeamconfig", "job", "create", "fileLevel", "--name", jobName, "--repoName", repoName, "--includeDirs", includeDirs] )

    @staticmethod
    def Delete(jobName):
        return subproccall( ["veeamconfig", "job", "delete", "--name", jobName ] )        

    @staticmethod
    def Start(jobName):
        res = subproccall( ["veeamconfig", "job", "start", "--name", jobName] )
        sessionId = None

        lines = res.split('\n')
        for ln in lines:
            if ln.find("Session ID:") != -1:
                first=ln.find("{")
                last = ln.find("}")
                sessionId = ln[first: last+1]

        return [res, sessionId]

    @staticmethod
    def List():
        return subproccall( ["veeamconfig", "job", "list"] )

    @staticmethod
    def DetailInfo(id):
        return subproccall( ["veeamconfig", "job", "info", "--id", id] )


class CJobInfo(object):
    def __init__(self, id, name, repoName):
        self.id = id
        self.name = name
        self.repoName = repoName

    def Id(self):
        return self.id

    def Name(self):
        return self.name

    def RepositoryName(self):
        return self.repoName

    def ToString(self):
        return "id='" +self.id + "' name='" + self.name + "' repositoryName='"+self.repoName + "'"

    def ToXmlNode(self):
        root = xml.Element("jobInfo")
        root.attrib["id"] = self.id
        root.attrib["name"] = self.name
        root.attrib["repositoryName"] = self.repoName
        return root

    def ToXml(self):
        root = self.ToXmlNode()
        return  xml.tostring(root, 'utf-8')        

class CJobInfoList(object):
    def __init__(self, list):
        self.list = list

    def List(self):
        return self.list

    @staticmethod
    def Get():
        text = CJob.List()
        lines = text.split("\n")
        list = [] # job info list
        for line in lines:
            if len(line) == 0:
                continue

            words = line.split()
            if len(words) == 0:
                continue
            if words[0].strip() == "Name":
                continue
            
            try:
                name = words[0].strip()
                id = words[1].strip()
                repoName = words[2].strip()

                list.append(CJobInfo(id, name, repoName))
            except:
                print "Failed to parse [", line, "]"

        return CJobInfoList(list)

    def ToXmlNode(self):
        root = xml.Element("jobInfoList")
        for jobInfo in self.list:
            root.append(jobInfo.ToXmlNode())
        return root

    def ToXml(self):
        root = self.ToXmlNode()
        return  xml.tostring(root, 'utf-8')


class CJobDetail(object):
    def __init__(self, text):
        self.text = text

    @staticmethod
    def Get(id):
        text = CJob.DetailInfo(id)
        return CJobDetail(text)

if __name__ == '__main__':
    pass