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
        text = 'You have successfully disabled custom user actions. ' \
               'Relaunch Espresso for the change to take effect.'
    else:
        # switch preference to true, or add it if it doesn't exist
        defaults.setBool_forKey_(True, 'TEAEnableUserActions')
        title = 'Custom User Actions Enabled'
        text = 'Please relaunch Espresso to load your custom actions.' \
               '\n\nChanges to your custom actions will be ' \
               'refreshed whenever you launch Espresso. If you add new ' \
               'files to your custom actions folder, you must relaunch ' \
               'Espresso TWICE for them to take effect. See the TEA wiki ' \
               'for more information:\n\n' \
               'http://wiki.github.com/onecrayon/tea-for-espresso'
    # Add or remove the symlinks
    bundle = NSBundle.bundleWithIdentifier_('com.onecrayon.tea.espresso')
    refresh_symlinks(bundle.bundlePath(), True)
    
    if notify:
        tea.say(context, title, text)
    return True
