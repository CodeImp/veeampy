#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
from exceptions import ValueError, RuntimeError

def subproccall(command):
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    except:
        print "Failed command: ",command
        raise

    res = p.communicate()

    if p.returncode != 0:
        if res[1] is not None:
            print "Failed command: ",command
            raise RuntimeError(res[1]+'\n'+res[0])
        else:
            print "Failed command: ",command
            raise ValueError(res[0]+'\n'+"Nonzero return code =", str(p.returncode))

    return res[0]

if __name__ == '__main__':
    pass