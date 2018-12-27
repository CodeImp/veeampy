from subproccall import *
from veeamlpb import session

class CBackup:
    @staticmethod
    def List():
        return subproccall(["veeamconfig", "backup", "list"])

    @staticmethod
    def Mount(id, dir):
        return subproccall( ["veeamconfig", "backup", "mount", "--id", id, "--mountDir", dir] )

class CBackupInfo(object):
    def __init__(self, name, id, startTime, finishTime):
        self.name = name
        self.id = id
        self.startTime = startTime
        self.finishTime = finishTime

class CBackupInfoList(object):
    def __init__(self, list):
        self.list = list

    @staticmethod
    def Get():
        text = CBackup.List()
        list = []
        lines = text.split('\n')
        del lines[0] #remove title

        for ln in lines:
            if len(ln) == 0:
                continue #skip last empty string

            nameLen = ln.find(" {")
            name = ln[0:nameLen].strip()

            idLen = ln.find("} ")
            id = ln[nameLen:idLen].split()

            timeWords = ln[idLen:0].split()

            startTime = timeWords[0]+" "+timeWords[1]
            finishTime = timeWords[2]+" "+timeWords[3]

            list.append(CBackupInfo(name, id, startTime, finishTime))

        return CBackupInfoList(list)

class CMountSession(object):
    def __init__(self):
        self.sessionId = None

    def Mount(self, backupId, mountDir):
        if self.sessionId != None:
            self.Umount()

        res = CBackup.Mount(backupId, mountDir)

        lines = res.split('\n')
        for ln in lines:
            if ln.find("Session ID:") != -1:
                first=ln.find("{")
                last = ln.find("}")
                self.sessionId = ln[first: last+1]

        return res

    def Umount(self):
        if self.sessionId == None:
            return 

        res = session.CSession.Stop(self.sessionId)
        self.sessionId = None
        return res

if __name__ == '__main__':
    pass