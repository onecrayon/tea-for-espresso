//
//  TEAUserInput.m
//  TEA for Espresso.sugar
//
//  Created by Ian Beck
//  http://onecrayon.com/tea/
//
//  MIT License
//

#import "TEAUserInput.h"
#import <EspressoTextActions.h>
#import <EspressoSyntaxCore.h>

// This allows me to set private getters and setters for the property
@interface TEAUserInput ()
@property (readwrite,copy) NSString *nib;
@property (readwrite,copy) NSString *defaultInput;
@property (readwrite,retain) id myContext;
@end


@implementation TEAUserInput

@synthesize customSheet;
@synthesize userInput;
@synthesize spinner;
@synthesize nib;
@synthesize defaultInput;
@synthesize myContext;

- (id)initWithDictionary:(NSDictionary *)dictionary bundlePath:(NSString *)myBundlePath {
	self = [super initWithDictionary:dictionary bundlePath:myBundlePath];
	if (self == nil)
		return nil;
	
	// Grab the target nib
	[self setNib:[dictionary objectForKey:@"nib"]];
	// Grab the default input
	[self setDefaultInput:[dictionary objectForKey:@"default_input"]];
	
	return self;
}

- (void)dealloc
{
	[self setCustomSheet:nil];
	[self setUserInput:nil];
	[self setSpinner:nil];
	[self setNib:nil];
	[self setDefaultInput:nil];
	[self setMyContext:nil];
	[super dealloc];
}

- (BOOL)performActionWithContext:(id)context error:(NSError **)outError {
	if ([self customSheet] == nil) {
		[NSBundle loadNibNamed:[self nib] owner:self];
	}
	// Set the default string in the user input
	if ([[self defaultInput] caseInsensitiveCompare:@"spacespertab"] == NSOrderedSame) {
		// Set the default number of spaces per tab from prefs
		NSUInteger num_spaces = [[context textPreferences] numberOfSpacesForTab];
		[self setDefaultInput:[NSString stringWithFormat:@"%lu", (unsigned long)num_spaces]];
	} else if ([self defaultInput] == nil) {
		[self setDefaultInput:@""];
	}
	[[self userInput] setStringValue:[self defaultInput]];
	
	[NSApp beginSheet:[self customSheet]
		   modalForWindow:[context windowForSheet]
		   modalDelegate:self
		   didEndSelector:@selector(sheetDidEnd:returnCode:contextInfo:)
		   contextInfo:nil
	];
	[self setMyContext:context];
	
	return YES;
}

- (IBAction) doSubmitSheet:(id)sender {
	[NSApp endSheet:[self customSheet] returnCode:1];
}

- (IBAction) cancel:(id)sender {
	[NSApp endSheet:[self customSheet] returnCode:0];
}

- (void)sheetDidEnd:(NSWindow *)sheet returnCode:(NSInteger)returnCode contextInfo:(void *)contextInfo {
	if (returnCode == 1) {
		// Doing this here, because Python might be starting up, which could take a while
		[[self spinner] startAnimation:self];
		[self initPython];
		
		// Send the info to TEAPythonLoader to run the action
		Class TEAPythonLoaderClass = NSClassFromString(@"TEAPythonLoader");
		
		// NOTE: in init, the instance gets a retain count of 1
		id actionLoader = [[TEAPythonLoaderClass alloc] init];
		BOOL returnValue = [actionLoader actInContext:[self myContext] forAction:self];
		
		// NOTE: release the actionLoader, decrementing its retain count to 0, which leads to its deallocation
		[actionLoader release];
	}
	
	[sheet orderOut:self];
}

@end
