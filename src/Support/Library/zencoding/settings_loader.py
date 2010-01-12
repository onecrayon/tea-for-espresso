'''
Zen settings loader that can read user-defined snippets from Espresso
@author: Sergey Chikuyonok (serge.che@gmail.com)
'''
import os
import re
import pickle

from Foundation import NSUserDefaults, NSLog

import stparser

plist_path = os.path.expanduser('~/Library/Preferences/com.macrabbit.Espresso.plist')
cache_folder = os.path.expanduser(
        '~/Library/Application Support/Espresso/Support/Caches'
)
cache_file = os.path.join(cache_folder, 'zen_user_snippets.cache')

re_full_tag = re.compile(r'^<([\w\-]+(?:\:\w+)?)((?:\s+[\w\-]+(?:\s*=\s*(?:(?:"[^"]*")|(?:\'[^\']*\')|[^>\s]+))?)*)\s*(\/?)>(?:</\1>)?')

_prev_settings = None

def _read_settings_from_app():
    defaults = NSUserDefaults.standardUserDefaults()
    snippets = defaults.objectForKey_('UserSnippets1.0')
    
    if snippets is not None:
        snips = {}
        abbrs = {}
        for item in snippets:
            if 'snippetString' in item and 'title' in item:
                abbr_name = 'triggerString' in item and item['triggerString'] or item['title']
                if re_full_tag.match(item['snippetString']):
                    abbrs[abbr_name] = item['snippetString']
                else:
                    snips[abbr_name] = item['snippetString']
        
        return {'common': {
            'snippets': snips,
            'abbreviations': abbrs
        }}
    
    return None

def load_settings():
    """
    Load zen coding's settings, combined with user-defined snippets
    """
    # First, check if the user even wants this to happen
    defaults = NSUserDefaults.standardUserDefaults()
    convert_to_zen = defaults.boolForKey_('TEAConvertUserSnippetsToZen')
    if convert_to_zen:
        orig_date = os.path.getmtime(plist_path)
        
        need_reload = globals()['_prev_settings'] is None
        
        # Does our cache path exist and is writable?
        cache_dir_exists = os.path.isdir(cache_folder)
        if not cache_dir_exists:
            # Attempt to create the cache folder
            try:
                os.makedirs(cache_folder, 0755)
                cache_dir_exists = True
            except os.error:
                NSLog('TEA Error: Cannot create zen coding cache path for user snippets')
        
        # In worst case scenario, we can't read or write to the cache file
        # so we'll need to read from preferences every time
        # This variable tracks the user snippets in case of that eventuality
        _data = None
        
        # check if cached file exists and up-to-date
        if cache_dir_exists and (not os.path.exists(cache_file) or \
           os.path.getmtime(cache_file) < orig_date):
            # need to reparse and cache data
            _data = _read_settings_from_app()
            try:
                fp = open(cache_file, 'wb')
                pickle.dump(_data, fp)
                fp.close()
            except IOError:
                NSLog('TEA Error: Zen user snippets cache file is not writable')
            need_reload = True
        
        if need_reload:
            try:
                fp = open(cache_file, 'rb')
                user_settings = pickle.load(fp)
                fp.close()
            except IOError:
                NSLog('TEA Error: Zen user snippets cache file is not readable')
                user_settings = _data
            globals()['_prev_settings'] = stparser.get_settings(user_settings)
            
        return globals()['_prev_settings']
    else:
        # They don't want to load in user snippets as zen snippets
        return stparser.get_settings()