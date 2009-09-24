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
	NSWindow *customSheet;
	NSTextField *numSpaces;
	NSProgressIndicator *spinner;
	id myContext;
}

@property (readonly,retain) IBOutlet NSWindow *customSheet;
@property (readonly,retain) IBOutlet NSTextField *numSpaces;
@property (readonly,retain) IBOutlet NSProgressIndicator *spinner;
@property (readonly,retain) id myContext;

- (void)sheetDidEnd:(NSWindow *)sheet returnCode:(NSInteger)returnCode contextInfo:(void *)contextInfo;

@end
