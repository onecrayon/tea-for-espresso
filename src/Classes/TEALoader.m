//
//  TEALoader.m
//  TEA for Espresso.sugar
//
//  Created by Ian Beck
//  http://onecrayon.com/tea/
//
//  MIT License

#import "TEALoader.h"
#import <EspressoTextActions.h>
#import <EspressoTextCore.h>


// Private setters
@interface TEALoader ()
@property (readwrite,copy) NSString* script;
@property (readwrite,copy) NSString* input;
@property (readwrite,copy) NSString* alternate;
@property (readwrite,copy) NSString* output;
@property (readwrite,copy) NSString* undo_name;
@end

@implementation TEALoader

@synthesize script;
@synthesize input;
@synthesize alternate;
@synthesize output;
@synthesize undo_name;

- (id)initWithDictionary:(NSDictionary *)dictionary bundlePath:(NSString *)myBundlePath {
	self = [super initWithDictionary:dictionary bundlePath:myBundlePath];
	if (self == nil)
		return nil;
	
	// Set loader's internal variables
	[self setScript:[dictionary objectForKey:@"script"]];
	[self setInput:[dictionary objectForKey:@"input"]];
	[self setAlternate:[dictionary objectForKey:@"alternate"]];
	[self setOutput:[dictionary objectForKey:@"output"]];
	[self setUndo_name:[dictionary objectForKey:@"undo_name"]];
	
	return self;
}

- (void)dealloc
{
	[self setScript:nil];
	[self setInput:nil];
	[self setAlternate:nil];
	[self setOutput:nil];
	[self setUndo_name:nil];
	[super dealloc];
}

- (BOOL)performActionWithContext:(id)context error:(NSError **)outError {
	if ([self script] == nil) {
		NSLog(@"TEA Error: no script found for TEALoader to invoke");
		return NO;
	}
	
	// Set up the base environmental variables
	NSMutableDictionary *env = [NSMutableDictionary dictionary];
	
	// Grab the URL-based variables
	NSURL *fileURL = [[context documentContext] fileURL];
	NSString *e_filepath = nil;
	NSString *e_filename = nil;
	NSString *e_directory = nil;
	if (fileURL != nil) {
		e_filename = [[fileURL path] lastPathComponent];
		if ([fileURL isFileURL]) {
			e_directory = [[fileURL path] stringByDeletingLastPathComponent];
			e_filepath = [fileURL path];
		}
	}
	
	// Set up the root zone selector
	NSString *e_root_zone = nil;
	if ([[[context syntaxTree] rootZone] typeIdentifier] != nil) {
		e_root_zone = [[[[context syntaxTree] rootZone] typeIdentifier] stringValue];
	}
	
	// Set up the preference variables
	id prefs = [context textPreferences];
	NSString *e_soft_tabs = nil;
	if ([prefs insertsSpacesForTab]) {
		e_soft_tabs = @"YES";
	} else {
		e_soft_tabs = @"NO";
	}
	NSString *e_tab_size = [NSString stringWithFormat:@"%d", [prefs numberOfSpacesForTab]];
	NSString *e_line_ending = [prefs lineEndingString];
	
	NSString *e_xhtml = nil;
	NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
	if ([defaults boolForKey:@"TEADefaultToXHTML"]) {
		e_xhtml = @"";
	} else {
		e_xhtml = [defaults stringForKey:@"TEASelfClosingString"];
	}
	
	// URL-based variables
	[self addObject:[self bundlePath] forKey:@"E_SUGARPATH" toDictionary:env];
	[self addObject:e_filepath forKey:@"E_FILEPATH" toDictionary:env];
	[self addObject:e_filename forKey:@"E_FILENAME" toDictionary:env];
	[self addObject:e_directory forKey:@"E_DIRECTORY" toDictionary:env];
	
	// Zone variables
	[self addObject:e_root_zone forKey:@"E_ROOT_ZONE" toDictionary:env];
	
	// Preference variables
	[self addObject:e_soft_tabs forKey:@"E_SOFT_TABS" toDictionary:env];
	[self addObject:e_tab_size forKey:@"E_TAB_SIZE" toDictionary:env];
	[self addObject:e_line_ending forKey:@"E_LINE_ENDING" toDictionary:env];
	[self addObject:e_xhtml forKey:@"E_XHTML" toDictionary:env];
	
	// Set up the user-defined environment variables
	for (NSDictionary *item in [defaults arrayForKey:@"TEAShellVariables"]) {
		[self addObject:[item objectForKey:@"value"] forKey:[item objectForKey:@"variable"] toDictionary:env];
	}
	
	// Initialize our common variables
	CETextRecipe *recipe = [CETextRecipe textRecipe];
	NSArray *ranges = [context selectedRanges];
	
	NSString *file = [self findScript:[self script]];
	if (file == nil) {
		NSLog(@"Error: TEALoader could not find script");
		return NO;
	}
	
	// Loop over the ranges and perform the script's action on each
	// Looping allows us to handle single ranges or multiple discontiguous selections
	for (NSValue *rangeValue in ranges) {
		NSRange range = [rangeValue rangeValue];
		// Add the items that change for each range
		[self addObject:[[context string] substringWithRange:range] forKey:@"E_SELECTED_TEXT" toDictionary:env];
		// ADD E_CURRENT_WORD?
		[self addObject:[[context string] substringWithRange:[[context lineStorage] lineRangeForRange:range]] forKey:@"E_CURRENT_LINE" toDictionary:env];
		[self addObject:[NSString stringWithFormat:@"%lu", (unsigned long)[[context lineStorage] lineNumberForIndex:range.location]] forKey:@"E_LINENUMBER" toDictionary:env];
		NSUInteger lineindex = range.location - [[context lineStorage] lineStartIndexForIndex:range.location lineNumber:nil];
		[self addObject:[NSString stringWithFormat:@"%lu", (unsigned long)lineindex] forKey:@"E_LINEINDEX" toDictionary:env];
		NSString *e_active_zone = nil;
		if ([[context syntaxTree] zoneAtCharacterIndex:range.location] != nil) {
			if ([[[context syntaxTree] zoneAtCharacterIndex:range.location] typeIdentifier] != nil) {
				e_active_zone = [[[[context syntaxTree] zoneAtCharacterIndex:range.location] typeIdentifier] stringValue];
			}
		}
		[self addObject:e_active_zone forKey:@"E_ACTIVE_ZONE" toDictionary:env];
		
		// Grab the contents for our STDIN
		
	}
}

- (BOOL)addObject:(id)myObject forKey:(NSString *)myKey toDictionary:(NSMutableDictionary*)dictionary {
	// If myKey is nil, sending it the length method will return 0
	if (myKey.length == 0) {
		return NO;
	}
	if (myObject == nil) {
		myObject = @"";
	}
	[dictionary setObject:myObject forKey:myKey];
	return YES;
}

@end
