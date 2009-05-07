#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Coda plug-in
Created on Apr 20, 2009

@author: sergey
'''
import os
from zencoding import zen_core
from zencoding.settings import zen_settings

zen_core.newline = os.getenv('CODA_LINE_ENDING', zen_core.newline)
zen_core.insertion_point = '$$IP$$'

cur_line = 'hello world div>p'
cur_index = 17

abbr = zen_core.find_abbr_in_line(cur_line, cur_index)
if abbr:
	print(zen_core.expand_abbr(abbr))
