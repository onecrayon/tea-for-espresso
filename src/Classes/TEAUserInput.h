//
//  TEAUserInput.h
//  TEA for Espresso.sugar
//
//  Created by Ian Beck
//  http://onecrayon.com/tea/
//
//  MIT License
//

#import <Cocoa/Cocoa.h>
#import "TEAforEspresso.h"


@interface TEAUserInput : TEAforEspresso {
	NSWindow *customSheet;
	NSTextField *userInput;
	NSProgressIndicator *spinner;
	NSString *nib;
	NSString *defaultInput;
	id myContext;
}

@property (retain) IBOutlet NSWindow *customSheet;
@property (retain) IBOutlet NSTextField *userInput;
@property (retain) IBOutlet NSProgressIndicator *spinner;
@property (readonly,copy) NSString *nib;
@property (readonly,copy) NSString *defaultInput;
@property (readonly,retain) id myContext;

- (IBAction) doSubmitSheet:(id)sender;
- (IBAction) cancel:(id)sender;
- (void)sheetDidEnd:(NSWindow *)sheet returnCode:(NSInteger)returnCode contextInfo:(void *)contextInfo;

@end
