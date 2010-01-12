#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zencoding.zen_editor import ZenEditor
from zencoding import zen_actions
import sys
import traceback
import tea_actions as tea

# This is a special variable; if it exists in a module, the module will be
# passed the actionObject as the second parameter
req_action_object = True

def act(context, actionObject, action_name, undo_name=None):
	zen_editor = ZenEditor(context)
	
	try:
		if action_name == 'expand_abbreviation':
			zen_actions.expand_abbreviation(zen_editor, zen_editor.get_syntax(), zen_editor.get_profile_name())
		elif action_name == 'wrap_with_abbreviation':
			abbr = actionObject.userInput().stringValue()
			if abbr:
				zen_actions.wrap_with_abbreviation(zen_editor, abbr, zen_editor.get_syntax(), zen_editor.get_profile_name())
		elif action_name == 'balance_in':
			zen_actions.match_pair(zen_editor, 'in')
		elif action_name == 'balance_out':
			zen_actions.match_pair(zen_editor, 'out')
		elif action_name == 'merge_lines':
			zen_actions.merge_lines(zen_editor)
		elif action_name == 'next_point':
			zen_actions.next_edit_point(zen_editor)
		elif action_name == 'prev_point':
			zen_actions.prev_edit_point(zen_editor)
		
	except:
		info = sys.exc_info()
		tea.log('%s: %s' % info[:2])
		tea.log(traceback.extract_tb(info[2]))
		
	return True