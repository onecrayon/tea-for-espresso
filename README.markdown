Text Editor Actions for Espresso
--------------------------------

Text Editor Actions (TEA) for Espresso is an [Espresso][1] plugin that provides:

1. Some of my favorite text actions for HTML, such as Wrap Selection In Tag
   (inspired mainly by Textmate's excellent HTML bundle)
2. Generic text manipulation scripts that can be leveraged by any Sugar (or
   through custom user actions)

TEA has been bundled with Espresso since version 1.0, so you do not need to
download it (unless you want to test bleeding edge improvements).

   [1]: http://macrabbit.com/espresso/

TEA for users
=============

Many people will be content with the default TEA HTML actions, but if you
wish you can add your own custom actions by defining them in XML (I plan to
add an interface for managing custom actions; until then you'll need to
use XML):

* [Adding your own actions][2]
* [A tutorial for adding simple tab completions][3]
* [Text snippets reference][4]
* [Third party snippet collections][5]
* [Adding or overriding Python scripts][6] (for more advanced custom actions)
* [Running shell scripts][7] (for advanced custom actions)

**Found something about TEA that makes you unhappy?** [Submit a bug report or
feature request][8] (requires free Lighthouse account) or visit the official
[TEA forum post][9].

   [2]: http://wiki.github.com/onecrayon/tea-for-espresso/adding-your-own-actions
   [3]: http://wiki.github.com/onecrayon/tea-for-espresso/adding-simple-tab-completions
   [4]: http://wiki.github.com/onecrayon/tea-for-espresso/text-snippets-reference
   [5]: http://wiki.github.com/onecrayon/tea-for-espresso/third-party-snippet-collections
   [6]: http://wiki.github.com/onecrayon/tea-for-espresso/adding-or-overriding-python-scripts
   [7]: http://wiki.github.com/onecrayon/tea-for-espresso/running-shell-scripts
   [8]: http://onecrayon.lighthouseapp.com/projects/28070-tea-espresso/tickets/new
   [9]: http://wiki.macrabbit.com/forums/viewthread/160/
   

TEA for Sugar developers
========================

There are three ways to leverage TEA within your own Sugar:

1. Use TEA's generic internal actions simply by adding XML definitions
(syntax is identical to custom user actions above; only difference is you
put your actions in your Sugar's TextActions folder). For a full list of
available actions, see the [generic action API][10].

2. Use the TEALoader class to run a custom script in any language supported
by the Mac OS X command line.  See [Running shell scripts][7] for more info.

3. Code your own Python scripts for TEA, leveraging the numerous built-in
helper functions.  See [Adding or overriding Python scripts][6] for more info.

   [10]: http://wiki.github.com/onecrayon/tea-for-espresso/generic-action-api

Errata
======

The [TEA for Espresso wiki][11] is currently the best place for information
about extending TEA. I do not yet have any documentation about using TEA's
bundled HTML actions; hopefully their names will be self-explanatory to some
extent.

If you are interested in coding your own Sugar in Python, the TEA for
Espresso project can also serve as an excellent starting point.  The
code is released under the MIT license, as described in the main bundle
file.

   [11]: http://wiki.github.com/onecrayon/tea-for-espresso