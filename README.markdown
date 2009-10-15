Text Editor Actions for Espresso
--------------------------------

Text Editor Actions (TEA) for Espresso is an [Espresso][1] plugin that 
provides numerous bundled actions and an infrastructure for easily creating 
more, whether you are a Sugar developer or not.

TEA has been bundled with Espresso since version 1.0, so you do not need to
download it (unless you want to test bleeding edge improvements).

For more info about TEA (including documentation) see the TEA website:

<http://onecrayon.com/tea/>

**Found something about TEA that makes you unhappy?** [Submit a bug report or
feature request][2] (requires free GitHub account) or [drop me a line][3].

   [1]: http://macrabbit.com/espresso/
   [2]: http://github.com/onecrayon/tea-for-espresso/issues
   [3]: http://onecrayon.com/about/contact/

Building from source
====================

Since you're here, odds are you want to mess around with TEA's source code. 
To compile TEA:

    git clone git://github.com/onecrayon/tea-for-espresso.git
    cd tea-for-espresso
    python setup.py py2app

If you wish to create a development version, you can run this instead:

    python setup.py py2app -A

This will create a normal version of the TEA plugin, but symlink all the 
internal files so that you don't have to rebuild the Sugar to try out changes 
(you'll still need to relaunch Espresso between changes, though).

To override the bundled version of TEA in Espresso, make sure to increment 
the CFBundleVersion in setup.py before compiling TEA.