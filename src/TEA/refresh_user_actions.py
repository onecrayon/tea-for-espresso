'''
Refreshes symlinks to user's Application Support directory to enable
custom user TEA actions
'''

import tea_actions as tea
from tea_utils import refresh_symlinks

def act(context, notify=True):
    '''
    Toggles custom user actions on and off and refreshes the symlinks
    
    If notify=True, will tell the user once the symlinks are generated
    '''
    defaults = NSUserDefaults.standardUserDefaults()
    enabled = defaults.stringForKey_('TEAEnableUserActions')
    if enabled is True:
        # switch preference to false
    else:
        # switch preference to true, or add it if it doesn't exist
    
    refresh_symlinks()
    
    if notify:
        tea.say(
            context, 'Custom User Actions Enabled',
            'You have successfully enabled custom user actions. '
            'Please relaunch Espresso in order to load your actions into TEA.'
        )
    return True
