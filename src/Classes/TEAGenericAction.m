//
//  TEAGenericAction.m
//  TEA for Espresso.sugar
//
//  Created by Ian Beck
//  http://onecrayon.com/tea/
//
//  MIT License
//

#import "TEAGenericAction.h"
#import "TEASymlinkHandler.h"

#import <EspressoTextActions.h>
#import <EspressoSyntaxCore.h>


// This allows us to set private setters for these variables
@interface TEAGenericAction ()
@property (readwrite,copy) NSString* syntaxContext;
@property (readwrite,copy) NSString* selectionContext;
@property (readwrite,copy) NSString* bundlePath;
@property (readwrite,copy) NSString* teaPath;
@property (readwrite,retain) NSArray* supportPaths;
@end

@implementation TEAGenericAction

@synthesize syntaxContext;
@synthesize selectionContext;
@synthesize bundlePath;
@synthesize teaPath;
@synthesize supportPaths;

- (id)initWithDictionary:(NSDictionary *)dictionary bundlePath:(NSString *)myBundlePath {
	self = [super init];
	if (self == nil)
		return nil;
	
	// Set up the syntax-context variable for later checking
	[self setSyntaxContext:[dictionary objectForKey:@"syntax-context"]];
	// Set up the selection-context variable for later checking
	[self setSelectionContext:[dictionary objectForKey:@"selection-context"]];
	// We need to remember the bundle path so we can check for scripts various places
	[self setBundlePath:myBundlePath];
	// Look up the TEA path
	[self setTeaPath:[[NSBundle bundleWithIdentifier:@"com.onecrayon.tea.espresso"] bundlePath]];
	
	// Sets up supportPaths, which tracks the possible locations of Support folders
	if (![[self bundlePath] isEqualToString:[self teaPath]]) {
		[self setSupportPaths:[NSArray arrayWithObjects:
								[@"~/Library/Application Support/Espresso/Support" stringByExpandingTildeInPath],
								[[self bundlePath] stringByAppendingPathComponent:@"Support"],
								[[self teaPath] stringByAppendingPathComponent:@"Support"],
								nil
							   ]];
	} else {
		[self setSupportPaths:[NSArray arrayWithObjects:
								[@"~/Library/Application Support/Espresso/Support" stringByExpandingTildeInPath],
								[[self bundlePath] stringByAppendingPathComponent:@"Support"],
								nil
							   ]];
	}
	
	return self;
}

- (void)dealloc
{
	[self setSyntaxContext:nil];
	[self setSelectionContext:nil];
	[self setBundlePath:nil];
	[self setTeaPath:nil];
	[self setSupportPaths:nil];
	[super dealloc];
}

- (BOOL)canPerformActionWithContext:(id)context {
	// Possible for context to be empty if it's partially initialized
	if ([context string] == nil) {
		return NO;
	}
	// Check on the syntaxContext
	if ([self syntaxContext] != nil) {
		NSRange range = [[[context selectedRanges] objectAtIndex:0] rangeValue];
		SXSelectorGroup *selectors = [SXSelectorGroup selectorGroupWithString:[self syntaxContext]];
		SXZone *zone = nil;
		if ([[context string] length] == range.location) {
			zone = [[context syntaxTree] rootZone];
		} else {
			zone = [[context syntaxTree] zoneAtCharacterIndex:range.location];
		}
		if (![selectors matches:zone]) {
			return NO;
		}
	}
	
	// Check on the selectionContext
	if ([self selectionContext] != nil) {
		// selectionContext might be none, one, one+, or multiple
		NSArray *ranges = [context selectedRanges];
		if ([ranges count] == 1) {
			if ([[self selectionContext] caseInsensitiveCompare:@"multiple"] == NSOrderedSame) {
				return NO;
			} else if (([[ranges objectAtIndex:0] rangeValue].length > 0) && ([[self selectionContext] caseInsensitiveCompare:@"none"] == NSOrderedSame)) {
				return NO;
			} else if (([[ranges objectAtIndex:0] rangeValue].length == 0) && ([[self selectionContext] caseInsensitiveCompare:@"one"] == NSOrderedSame || [[self selectionContext] caseInsensitiveCompare:@"one+"] == NSOrderedSame)) {
				return NO;
			}
		} else if (([[self selectionContext] caseInsensitiveCompare:@"multiple"] != NSOrderedSame) || ([[self selectionContext] caseInsensitiveCompare:@"one+"] != NSOrderedSame)) {
			return NO;
		}
	}
	
	// Everything must have checked out
	return YES;
}

- (NSString *)findScript:(NSString *)fileName inFolders:(NSArray *)folders {
	// Make sure the script has .py on the end
	if ([[fileName pathExtension] isEqualToString:@"py"]) {
		// The caller has the responsibility for the memory management of parameters, this is correct.
		fileName = [fileName stringByAppendingPathExtension:@"py"];
	}
	// Iterate over the array and check if the paths exist
	NSString *path = nil;
	
	for (NSString* supportPath in [self supportPaths]) {
		for (NSString* testPath in folders) {
			NSString *targetPath = [[supportPath stringByAppendingPathComponent:testPath] stringByAppendingPathComponent:fileName];
			if ([[NSFileManager defaultManager] fileExistsAtPath:targetPath]) {
				path = targetPath;
				break;
			}
		}
		if (path != nil) {
			break;
		}
	}
	
	return path;
}

- (NSString *)findScript:(NSString *)fileName {
	return [self findScript:fileName inFolders:[NSArray arrayWithObjects:@"Scripts", nil]];
}

@end
