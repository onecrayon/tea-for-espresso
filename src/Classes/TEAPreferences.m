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
#import "TEASymlinkHandler.h"

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
@synthesize versionInfo;

- (void)awakeFromNib
{
	NSString *version = [[NSBundle bundleWithIdentifier:@"com.onecrayon.tea.espresso"] objectForInfoDictionaryKey:@"CFBundleVersion"];
	[versionInfo setStringValue:[NSString stringWithFormat:@"version %@", version]];
}

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
	// Performs the symlink refresh when user actions are toggled
	[[TEASymlinkHandler sharedHandler] rebuild];
}

- (IBAction)customActionsHelp:(id)sender
{
	// Opens URL with help info for custom user actions
	NSString *url = @"http://onecrayon.com/tea/docs/";
	[[NSWorkspace sharedWorkspace] openURL:[NSURL URLWithString:url]];
}

@end

