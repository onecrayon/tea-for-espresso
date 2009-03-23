Text Editor Actions for Espresso
--------------------------------

Text Editor Actions (TEA) for Espresso (originally Textmate Emulation
Actions) are some of the text manipulation actions that
I think every text editor should have, implemented as an [Espresso][1]
Sugar. I originally began work on TEA because I wanted to use Espresso
but couldn't bear to abandon some of my favorite Textmate workflows, but
it has since grown into a general use platform for extending the application
in ways useful to my everyday work as a web developer.

TEA for Espresso is currently in an early testing stage; please see the
[TEA for Espresso forum post][2] for download information, known bugs,
and more.

If you are interested in extending or modifying TEA for Espresso
for your own use, then you've come to the right place.

   [1]: http://macrabbit.com/espresso/
   [2]: http://wiki.macrabbit.com/forums/viewthread/160/

Extending TEA for Espresso
==========================

TEA for Espresso is coded in [Python][3] and can be easily extended with
your own custom actions either by writing your own Python scripts, by defining
new actions for existing scripts in a simple XML file, or by
editing the TEA for Espresso Actions.xml file to tweak existing actions
to your liking.  For more information, see the [wiki][4]:

* [Installing third party snippet collections][7]
* [Defining new actions via XML][5]
* [Adding or overriding Python scripts][6]

   [3]: http://python.org/
   [4]: http://wiki.github.com/onecrayon/tea-for-espresso
   [5]: http://wiki.github.com/onecrayon/tea-for-espresso/adding-your-own-actions
   [6]: http://wiki.github.com/onecrayon/tea-for-espresso/adding-or-overriding-python-scripts
   [7]: http://wiki.github.com/onecrayon/tea-for-espresso/third-party-snippet-collections

If you are instead interested in coding your own
Sugar in Python, the TEA for Espresso project can also serve as an excellent
starting point.  The code is released under the MIT license, as described in
the main bundle file.