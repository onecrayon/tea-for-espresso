//
//  TEASpacesToTabs.h
//  TEA for Espresso.sugar
//
//  Created by Ian Beck
//  http://onecrayon.com/tea/
//
//  MIT License
//

#import <Cocoa/Cocoa.h>
#import "TEAforEspresso.h"


@interface TEASpacesToTabs : TEAforEspresso {
	(IBOutlet) customSheet;
	(IBOutlet) numSpaces;
	(IBOutlet) spinner;
	(id) myContext;
}

@property (readonly,retain) id myContext;

@end
