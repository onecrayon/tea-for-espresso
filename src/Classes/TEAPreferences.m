//
//  TEAPreferences.m
//  TEA for Espresso.sugar
//
//  Created by Ian Beck
//  http://onecrayon.com/tea/
//
//  MIT License
//

#import "TEAPreferences.h"
#import <BWToolkitFramework/BWToolkitFramework.h>


// This allows us to set private setters for these variables
@interface TEAPreferences ()
@property (readwrite,retain) NSWindowController* prefs;
@end

@implementation TEAPreferences

@synthesize prefs;

- (id)initWithDictionary:(NSDictionary *)dictionary bundlePath:(NSString *)myBundlePath {
	self = [super init];
	if (self == nil)
		return nil;
	return self;
}

- (BOOL)performActionWithContext:(id)context error:(NSError **)outError {
	[self setPrefs:[[TEAPreferencesController alloc] initWithWindowNibName:@"TEAPreferences"]];
	[prefs setShouldCascadeWindows:NO];
	[[prefs window] setFrameAutosaveName:@"TEAPreferences"];
	[prefs showWindow:self];
	[prefs retain];
	return YES;
}

- (BOOL)canPerformActionWithContext:(id)context {
	return YES;
}

@end

// ==========================================================

// The window controller
@implementation TEAPreferencesController

@synthesize arrayController;
@synthesize tableView;

- (IBAction)addListItem:(id)sender {
	// Adds an item to the table and immediately selects it for editing
	[[self arrayController] add:sender];
	[self performSelector:@selector(editInsertedRowInTable:) withObject:[self tableView] afterDelay:0];
}

- editInsertedRowInTable:(NSTableView *)targetTable {
	// Edits the most recently inserted row; many thanks to Todd Ransom for pointing me in this direction!
	NSUInteger row = [[[self arrayController] arrangedObjects] count] - 1;
	[[self arrayController] setSelectionIndex:row];
	[targetTable editColumn:0 row:[targetTable selectedRow] withEvent:nil select:YES];
}

- (IBAction) toggleUserActions:(id)sender {
	// TODO: Figure out if I need this action at all
	// Performs the symlink refresh when user actions are toggled
	NSBundle *bundle = [NSBundle bundleWithIdentifier:@"com.onecrayon.tea.espresso"];
	// Use the bundle to refresh symlinks; Python original: refresh_symlinks(bundle.bundlePath(), True)
}

- (IBAction) customActionsHelp:(id)sender {
	// Opens URL with help info for custom user actions
	NSString *url = @"http://onecrayon.com/tea/docs/";
	[[NSWorkspace sharedWorkspace] openURL:[NSURL URLWithString:url]];
}

- (void) windowWillClose:(NSNotification *)notification {
	[self autorelease];
}

@end

// ==========================================================

// This allows us to transform nil values to empty strings

@implementation TEANilToString

+ (Class)transformedValueClass {
	return [NSString class];
}

+ (BOOL)allowsReverseTransformation {
	return YES;
}

- (NSString *)transformedValue:(id)value {
	return value;
}

- (NSString *)reverseTransformedValue:(id)value {
	if (value == nil) {
		return @"";
	} else {
		return value;
	}
}

@end

