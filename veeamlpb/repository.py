#!/usr/bin/python
# -*- coding: utf-8 -*-

from veeamlpb.subproccall import subproccall

import xml.etree.ElementTree as xml

class CRepository:
    @staticmethod
    def List():
        return subproccall( ["veeamconfig", "repository", "list"] )

    @staticmethod
    def Create(name, location):
        print subproccall( ["veeamconfig", "repository", "create", "--name", name, "--location", location] )

    @staticmethod
    def Delete (id):
        print subproccall(["veeamconfig", "repository", "delete", "--answer", "yes", "--id", id] )

class CRepositoryInfo(object):
    def __init__(self, id, type, name, location, accessable, backupServer):
        self.id = id
        self.type = type
        self.name = name
        self.location = location
        self.accessable =accessable
        self.backupServer = backupServer

    def Id(self):
        return self.id

    def Type(self):
    	return self.type

    def Name(self):
        return self.name

    def Location(self):
        return self.location

    def Accessable(self):
        return self.accessable

    def BaclupServer(self):
        return self.backupServer

    def ToString(self):
        return "id='" +self.id + "' type='" + self.type + "' name='"+self.name + "' location='" + self.location + "' accessable='" + self.accessable + "' backupServer='" + self.backupServer + "'"

    def ToXmlNode(self):
        root = xml.Element("repositoryInfo")
        root.attrib["id"] = self.id
        root.attrib["type"] = self.type
        root.attrib["name"] = self.name
        root.attrib["location"] = self.location
        root.attrib["accessable"] = self.accessable
        root.attrib["backupServer"] = self.backupServer
        return root

    def ToXml(self):
        root = self.ToXmlNode()
        return  xml.tostring(root, 'utf-8')        


class CRepositoryList(object):
    def __init__(self, list):
        self.list = list

    def List(self):
        return self.list

    def ToXmlNode(self):
        root = xml.Element("repositoryInfoList")
        for repositoryInfo in self.list:
            root.append(repositoryInfo.ToXmlNode())
        return root

    def ToXml(self):
        root = self.ToXmlNode()
        return  xml.tostring(root, 'utf-8')

    @staticmethod
    def Get():
        text = CRepository.List()
        lines = text.split("\n")
        list = [] # repository info list
        for line in lines:
            if len(line) == 0:
                continue

            words = line.split()
            if len(words) == 0:
                continue
            if words[0] == "Name":
                continue

            try:
                name = words[0]
                id = words[1]
                location = words[2]
                type = words[3]                
                accessable = words[4]

                backupServer = ""
                if (len(words) > 5):
                    backupServer = words[5]

                list.append(CRepositoryInfo(id, type, name, location, accessable, backupServer))
            except:
                print "Failed to parse [", line, "]"        
        return CRepositoryList(list)


if __name__ == '__main__':
    pass