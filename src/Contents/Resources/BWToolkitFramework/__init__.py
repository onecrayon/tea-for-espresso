'''
Python mapping for the BWToolkit framework.

Many thanks to Johan Rydberg
<http://github.com/jrydberg/pyobjc-bwtoolkitframework/>
'''

import os.path

from Framework import NSBundle
import objc
 
__bundle__ = objc.initFrameworkWrapper("BWToolkitFramework",
    frameworkIdentifier="com.brandonwalkin.BWToolkitFramework",
    frameworkPath=objc.pathForFramework(
		os.path.join(
	        NSBundle.bundleWithIdentifier_('com.onecrayon.tea.espresso').bundlePath(),
			"Contents",
			"Frameworks", 
			"BWToolkitFramework.framework"
		)
	),
    globals=globals()
)