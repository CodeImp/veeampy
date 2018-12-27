#!/usr/bin/python
# -*- coding: utf-8 -*-

from veeamlpb.subproccall import subproccall

class CVersion(object):
    def __init__(self, str):
        self.str = ""

        if str[0] == 'v':
            self.str = str[1:-1]
        else:
            self.str = str

        [self.major, self.minor, self.revision, self.build] = self.str.split('.')

    def ToString(self):
        return self.str
    def Major(self):
        return self.major
    def Minor(self):
        return self.minor
    def Revision(self):
        return self.revision
    def Build(self):
        return self.build

    @staticmethod
    def Get():
        text = subproccall(["veeamconfig", "version"])
        return CVersion(text)

if __name__ == '__main__':
    pass