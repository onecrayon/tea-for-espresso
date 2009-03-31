'''
Refreshes symlinks to user's Application Support directory to enable
custom user TEA actions
'''

from Foundation import *

import tea_actions as tea
from tea_utils import refresh_symlinks

def act(context, notify=True):
    '''
    Toggles custom user actions on and off and refreshes the symlinks
    
    If notify=True, will tell the user once the symlinks are generated
    '''
    defaults = NSUserDefaults.standardUserDefaults()
    enabled = defaults.boolForKey_('TEAEnableUserActions')
    if enabled:
        # switch preference to false
        defaults.setBool_forKey_(False, 'TEAEnableUserActions')
        title = 'Custom User Actions Disabled'
        text = 'You have successfully disabled custom user actions. Relaunch '
               'Espresso to remove your actions from the menus.'
    else:
        # switch preference to true, or add it if it doesn't exist
        defaults.setBool_forKey_(True, 'TEAEnableUserActions')
        title = 'Custom User Actions Enabled'
        text = 'You have successfully enabled custom user actions. '
               'You must relaunch Espresso in order to load your custom '
               'actions.\n\nChanges to your custom actions will be refreshed '
               'whenever you relaunch Espresso. If you add files to your custom '
               'action folder, you will need to relaunch Espresso twice for '
               'them to take effect.'
    # Add or remove the symlinks
    refresh_symlinks(True)
    
    if notify:
        tea.say(context, title, text)
    return True
