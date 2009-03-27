'''
Refreshes symlinks to user's Application Support directory to enable
custom user TEA actions
'''

import tea_actions as tea
from tea_utils import refresh_symlinks

def act(context, notify=True):
    '''If notify=True, will tell the user once the symlinks are generated'''
    refresh_symlinks()
    tea.say(
        context, 'Custom User Actions Enabled',
        'You have successfully enabled custom user actions. '
        'Please relaunch Espresso in order to load your actions into TEA.'
    )
