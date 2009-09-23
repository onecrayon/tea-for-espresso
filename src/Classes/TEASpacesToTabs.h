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
	IBOutlet NSWindow *customSheet;
	IBOutlet NSTextField *numSpaces;
	IBOutlet NSProgressIndicator *spinner;
	id myContext;
}

@property (readonly,retain) id myContext;

- (void)sheetDidEnd:(NSWindow *)sheet returnCode:(NSInteger)returnCode contextInfo:(void *)contextInfo;

@end
