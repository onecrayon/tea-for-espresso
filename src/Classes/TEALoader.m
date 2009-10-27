//
//  TEALoader.m
//  TEA for Espresso.sugar
//
//  Created by Ian Beck
//  http://onecrayon.com/tea/
//
//  MIT License

#import "TEALoader.h"


// Private setters
@interface TEALoader ()
@property (readwrite,copy) NSString* script;
@property (readwrite,copy) NSString* input;
@property (readwrite,copy) NSString* alt;
@property (readwrite,copy) NSString* output;
@property (readwrite,copy) NSString* undo;
@end

@implementation TEALoader

@synthesize script;
@synthesize input;
@synthesize alt;
@synthesize output;
@synthesize undo;

- (id)initWithDictionary:(NSDictionary *)dictionary bundlePath:(NSString *)myBundlePath {
	self = [super initWithDictionary:dictionary bundlePath:myBundlePath];
	if (self == nil)
		return nil;
	
	// Set loader's internal variables
	[self setScript:[dictionary objectForKey:@"script"]];
	[self setInput:[dictionary objectForKey:@"input"]];
	[self setAlt:[dictionary objectForKey:@"alternate"]];
	[self setOutput:[dictionary objectForKey:@"output"]];
	[self setUndo:[dictionary objectForKey:@"undo_name"]];
	
	return self;
}

- (BOOL)performActionWithContext:(id)context error:(NSError **)outError {
	if ([self script] == nil) {
		NSLog(@"TEA Error: no script found for TEALoader to invoke");
		return NO;
	}
	
	// Set up the base environmental variables
	NSMutableDictionary *base_env = [NSMutableDictionary dictionary];
	
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
	if [[[context syntaxTree] rootZone] typeIdentifier] != nil) {
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
	[self addObject:[self bundlePath] forKey:@"E_SUGARPATH" toDictionary:base_env];
	[self addObject:e_filepath forKey:@"E_FILEPATH" toDictionary:base_env];
	[self addObject:e_filename forKey:@"E_FILENAME" toDictionary:base_env];
	[self addObject:e_directory forKey:@"E_DIRECTORY" toDictionary:base_env];
	
	// Zone variables
	[self addObject:e_root_zone forKey:@"E_ROOT_ZONE" toDictionary:base_env];
	
	// Preference variables
	[self addObject:e_soft_tabs forKey:@"E_SOFT_TABS" toDictionary:base_env];
	[self addObject:e_tab_size forKey:@"E_TAB_SIZE" toDictionary:base_env];
	[self addObject:e_line_ending forKey:@"E_LINE_ENDING" toDictionary:base_env];
	[self addObject:e_xhtml forKey:@"E_XHTML" toDictionary:base_env];
	
	// Set up the user-defined environment variables
	for (NSString *item in [defaults arrayForKey:@"TEAShellVariables"]) {
		[self addObject:[item objectForKey:@"value"] forKey:[item objectForKey:@"variable"] toDictionary:base_env];
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
		
		
	}
}

- (BOOL)addObject:(id)myObject forKey:(id)myKey toDictionary:(NSMutableDictionary*)dictionary {
	if (myKey == nil || [myKey compare:@""] == NSOrderedSame) {
		return NO;
	}
	if (myObject == nil) {
		myObject = @"";
	}
	[dictionary setObject:myObject forKey:myKey];
	return YES;
}

@end
