#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zencoding.zen_editor import ZenEditor
from zencoding import zen_core as zen_coding

# This is a special variable; if it exists in a module, the module will be
# passed the actionObject as the second parameter
req_action_object = True

def act(context, actionObject, action_name, undo_name=None):
	zen_editor = ZenEditor(context)
	
	if action_name == 'wrap_with_abbreviation':
		abbr = actionObject.userInput().stringValue()
		if abbr:
			return zen_coding.run_action(action_name, zen_editor, abbr)
	else:
		return zen_coding.run_action(action_name, zen_editor)
			
	return False