'''
Wrap Selection in Tag
A Default Action

Wraps the currently selected text in a tag supplied by the user
'''

import tea_util as tea

def act(context):
    '''Required method; performs the action'''
    context.insertTextSnippet_(tea.snippet('<#{1:p}>SELECTED_TEXT</#{1/\s.*//}>#0'))
#     ranges = context.selectedRanges()
#     for range in ranges:
#         print(range)
    
#     response = tea.say(context, 'Success!',
#                        'Successfully ran Wrap Selection as Tag')
    return True
