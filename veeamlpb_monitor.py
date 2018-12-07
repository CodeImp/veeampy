#!/usr/bin/python
# -*- coding: utf-8 -*-

import veeamlpb
import os

def checkVersion():
    version = veeamlpb.version.CVersion.Get()
    print "veeam Agent for Linux versin ",version.ToString()

def EnumerateSession():
    print "---"
    print "Enumerate sessions:"
    sessions = veeamlpb.session.CSessionInfoList.Get()
    for sessionInfo in sessions.List():
        print sessionInfo.ToString()


        print "Find session by id:"
        newSessionInfo = veeamlpb.session.CSessionInfo.GetById(sessionInfo.Id())
        print newSessionInfo.ToString()    

def EnumerateRepositories():
    print "---"
    print "Enumerate repositories:"
    repositoryList = veeamlpb.repository.CRepositoryList.Get()
    for repoInfo in repositoryList.List():
        print repoInfo.ToString()

def EnumerateJobs():
    print "---"
    print "Enumerate jobs:"
    jobs = veeamlpb.job.CJobInfoList.Get()
    for jobInfo in jobs.List():
        print jobInfo.ToString()

def SendXmlsessions():

    print "---"
    print "Session list in XML format:"

    sessions = veeamlpb.session.CSessionInfoList.Get()
    text = sessions.ToXml()
    print text

    sessionsFileName = "session_list.xml"
    print "Store XML to file: ",sessionsFileName
    sessionsXmlFile = open(sessionsFileName, "w")
    sessionsXmlFile.write(text)
    sessionsXmlFile.close()

    hostname = os.uname()[1]
    target = "user@deb-iscsi-test:/home/user"
    os.system("scp ./"+sessionsFileName+" "+target+"/backups/"+hostname+"/session_list.xml")


def SendMailsessions():
    print "---"
    print "Sending statistic to administrator:"

    sessions = veeamlpb.session.CSessionInfoList.Get()

    #recipient = "Sergey.Shtepa@veeam.com"
    recipient = "dear.admin@company.com"
    subject = "VAL status notification"
    text = "Statistic:\n"

    inx = 0;
    successCount = 0
    warningCount = 0
    errorCount = 0

    for sessionInfo in sessions.List():
        if (sessionInfo.State() == "Success"):
            successCount += 1
        elif (sessionInfo.status == "Warning"):
            warningCount += 1
        else:
            errorCount += 1
    text += str(successCount)+"/"+str(warningCount)+"/"+str(errorCount)+" Success/Warning/Error\n"

    text += "Last 10 session:\n"
    for sessionInfo in reversed(sessions.List()):
        if inx == 10:
            text += "...\n"
            break;

        text += str(inx)+" | "+sessionInfo.State()+" | "+sessionInfo.JobName()+" | "+sessionInfo.StartTime()+" / "+sessionInfo.FinishTime() + "\n"
        #text += 
        inx += 1

    text += "\n"
    text += "--------------------------------------------------------------------------------\n"
    text += "  Yours sincerely, Veeam Agent Linux monitor\n"

    print text
    #os.system("echo '"+text+"' | mail -s '"+subject+"' "+recipient)


def main():
    checkVersion()

    #EnumerateSession()
    #EnumerateRepositories()
    #EnumerateJobs()

    SendXmlsessions()

    SendMailsessions()
    return 0;

result = main()
print "Complete with code",result
exit(result)
