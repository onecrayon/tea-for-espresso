#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
sys.path.append(os.getenv('TM_BUNDLE_SUPPORT'))

from zencoding import zen_core
from zencoding.settings import zen_settings

zen_core.newline = os.getenv('TM_LINE_ENDING', zen_core.newline)

point_ix = 0
def place_ins_point(text):
	globals()['point_ix'] += 1
	return '$%s' % point_ix

zen_core.insertion_point = place_ins_point
zen_core.sub_insertion_point = place_ins_point

cur_line = os.getenv('TM_CURRENT_LINE', '')
cur_index = int(os.getenv('TM_LINE_INDEX', 0))
scope = os.getenv('TM_SCOPE')

if 'xsl' in scope:
	doc_type = 'xsl'
else:
	doc_type = re.findall(r'\bhtml|css|xml\b', scope)[-1]
	
# doc_type = re.search(r'\b(html|css|xml|xsl)\b', scope)
if not doc_type:
	doc_type = 'html'

abbr, start_index = zen_core.find_abbr_in_line(cur_line, cur_index)
if abbr:
	result = cur_line[0:start_index] + zen_core.expand_abbr(abbr, doc_type)
	cur_line_pad = re.match(r'^(\s+)', cur_line)
	if cur_line_pad:
		result = zen_core.pad_string(result, cur_line_pad.group(1))
	
	sys.stdout.write(result + cur_line[cur_index:])
else:
	sys.stdout.write(cur_line[0:cur_index] + zen_settings['indentation'] + '$0' + cur_line[cur_index:])