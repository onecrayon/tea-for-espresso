'''
Class that enables persistent regex evaluations

Usage:
gre = persistent_re()

if gre.match(r'foo', text):
    # do something with gre.last, which is an re MatchObject
'''

import re

class persistent_re(object):
    def __init__(self):
        self.last = None
    def match(self, pattern, text):
        self.last = re.match(pattern, text)
        return self.last
    def search(self, pattern, text):
        self.last = re.search(pattern, text)
        return self.last
