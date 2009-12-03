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

// ==========================================================

// This allows us to transform nil values to empty strings

@implementation TEANilToString

+ (void)load
{
	[super load];
	
	TEANilToString *transformer = [[TEANilToString alloc] init];
	[NSValueTransformer setValueTransformer:transformer forName:@"TEANilToString"];
	[transformer release];
}

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


@implementation TEAPreferencesViewController

@synthesize arrayController;
@synthesize tableView;

- (IBAction)addListItem:(id)sender
{
	// Adds an item to the table and immediately selects it for editing
	[[self arrayController] add:sender];
	[self performSelector:@selector(editInsertedRowInTable:) withObject:[self tableView] afterDelay:0];
}

- (void)editInsertedRowInTable:(NSTableView *)targetTable
{
	// Edits the most recently inserted row; many thanks to Todd Ransom for pointing me in this direction!
	NSUInteger row = [[[self arrayController] arrangedObjects] count] - 1;
	[[self arrayController] setSelectionIndex:row];
	[targetTable editColumn:0 row:[targetTable selectedRow] withEvent:nil select:YES];
}

- (IBAction)toggleUserActions:(id)sender
{
	// TODO: Figure out if I need this action at all
	// Performs the symlink refresh when user actions are toggled
	NSBundle *bundle = [NSBundle bundleWithIdentifier:@"com.onecrayon.tea.espresso"];
	// Use the bundle to refresh symlinks; Python original: refresh_symlinks(bundle.bundlePath(), True)
}

- (IBAction)customActionsHelp:(id)sender
{
	// Opens URL with help info for custom user actions
	NSString *url = @"http://onecrayon.com/tea/docs/";
	[[NSWorkspace sharedWorkspace] openURL:[NSURL URLWithString:url]];
}

@end

