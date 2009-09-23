//
//  TEASpacesToTabs.m
//  TEA for Espresso.sugar
//
//  Created by Ian Beck
//  http://onecrayon.com/tea/
//
//  MIT License
//

#import "TEASpacesToTabs.h"

// This allows me to set private getters and setters for the property
@interface TEAGenericAction ()
@property (readwrite,retain) id myContext;
@end


@implementation TEASpacesToTabs

@synthesize myContext;

- (BOOL)performActionWithContext:(id)context error:(NSError **)outError {
	if ([self customSheet] != nil) {
		[NSBundle loadNibNamed:@"TEASpacesPerTabsSheet" owner:self];
		// Set the default number of spaces per tab from prefs
		NSUInteger num_spaces = [[context textPreferences] numberOfSpacesForTab];
		[[self numSpaces] setStringValue:[NSString stringWithFormat:@"%d", num_spaces]];
		[NSApp beginSheet:[self customSheet]
		       modalForWindow:[context windowForSheet]
			   modalDelegate:self,
		       didEndSelector:@selector(sheetDidEnd:returnCode:contextInfo:)
			   contextInfo:nil
		];
		[self setMyContext:context];
	}
	return YES;
}

- (IBAction) doSubmitSheet:(id)sender {
	[NSApp endSheet:[self customSheet] returnCode:1];
}

- (IBAction) cancel:(id)sender {
	[NSApp endSheet:[self customSheet] returnCode:0];
}

- (void)sheetDidEnd:(NSWindow *)sheet returnCode:(NSInteger)returnCode contextInfo:(void *)contextInfo {
	[self initPython];
	
	if (returnCode == 1) {
		// Send the info to TEAPythonLoader to run the action
		Class TEAPythonLoaderClass = NSClassFromString(@"TEAPythonLoader");
		id actionLoader = [[TEAPythonLoaderClass alloc] init];
		(BOOL) returnValue = [actionLoader actInContext:[self myContext] forAction:self];
	}
	
	[sheet orderOut:self];
}

@end
