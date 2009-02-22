'''
Wrap Selection in Tag
A Default Action

Wraps the currently selected text in a tag supplied by the user
'''

import tea_util as tea

def act(context):
    response = tea.say(context, 'Success!',
                       'Successfully ran Wrap Selection as Tag')
    return True
