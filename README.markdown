Text Editor Actions for Espresso
--------------------------------

**This version of TEA for Espresso is officially deprecated as of
[Espresso 2.0](http://macrabbit.com/espresso/2/).** If you are interested
in leveraging TEA, please email MacRabbit for more information.

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
To compile TEA first clone it from GitHub (if you don't have Git installed,
[download it instead][4]):

    git clone git://github.com/onecrayon/tea-for-espresso.git

   [4]: http://code.google.com/p/git-osx-installer/

In order to compile, TEA for Espresso needs to know where your Espresso
installation lives.  By default it will look in your `/Applications` folder,
but if you have Espresso installed somewhere else, you can create a
symbolic link to it that the compiler will follow like this:

    ln -s /path/to/Espresso.app /Applications/Espresso.app

To compile, just open the Xcode project and hit the build button!

To override the bundled version of TEA in Espresso, make sure to increment 
the CFBundleVersion in Info.plist before compiling TEA.