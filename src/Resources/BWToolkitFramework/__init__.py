'''
Python mapping for the BWToolkit framework.
'''

import os.path

from Foundation import NSBundle
import objc

objc.loadBundle("BWToolkitFramework",
	globals(),
    bundle_path=objc.pathForFramework(
        os.path.join(
            NSBundle.bundleWithIdentifier_('com.onecrayon.tea.espresso').bundlePath(),
            "Contents",
            "Frameworks", 
            "BWToolkitFramework.framework"
        )
    )
)