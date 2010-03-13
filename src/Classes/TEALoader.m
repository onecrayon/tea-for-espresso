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
#import <NSString+MRFoundation.h>


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

// Tests if the unichar character is alphanumeric or one of these punctuation marks: _-#.>+*:$!@
- (BOOL) isWordCharacter:(unichar)character {
	NSCharacterSet *alphaNumericChars = [NSCharacterSet alphanumericCharacterSet];
	NSCharacterSet *punctuation = [NSCharacterSet characterSetWithCharactersInString:@"_-#.>+*:$!@"];
	
	return ([alphaNumericChars characterIsMember:character] || [punctuation characterIsMember:character]);
}

// Tests from start of the line to index to see if index is part of an HTML tag
- (BOOL) lineToIndexEndsWithTag:(NSUInteger)index inContext:(id)context {
	unichar character = [[context string] characterAtIndex:index];
	// Impossible for the line to the index to be an HTML tag if the character isn't a caret
	if (character != '>') {
		return NO;
	}
	NSUInteger linestart = [[context lineStorage] lineStartIndexLessThanIndex:index];
	NSString *text = [[context string] substringWithRange:NSMakeRange(linestart, index - linestart + 1)];
	// I don't know which (if any) regex libraries are included in Espresso, so here's a hack with NSPredicate
	// NSPredicate regex test courtesy of: http://www.stiefels.net/2007/01/24/regular-expressions-for-nsstring/
	// Using double backslashes to escape them
	NSString *regex = @".*(<\\/?[\\w:-]+[^>]*|\\s*(/|\\?|%|-{2,3}))>";
	NSPredicate *regextest = [NSPredicate predicateWithFormat:@"SELF MATCHES %@", regex];
	
	return [regextest evaluateWithObject:text];
}

// Get the word in the current context around the given index; the range is returned by reference
// Usage: NSRange my_range; [self getWordAtIndex:index inContext:context forRange:&my_range];
- (NSString *)getWordAtIndex:(NSUInteger)cursor inContext:(id)context forRange:(NSRange *)range {
	NSMutableString *word = [NSMutableString stringWithString:@""];
	NSUInteger maxindex = [[context string] length] - 1;
	unichar character;
	BOOL inword = NO;
	NSInteger index = cursor;
	NSUInteger firstindex, lastindex;
	if (index != maxindex) {
		// Check if index is mid-word
		character = [[context string] characterAtIndex:index+1];
		if ([self isWordCharacter:character]) {
			inword = TRUE;
			// Parse forward until we hit the end of the word or document
			while (inword) {
				character = [[context string] characterAtIndex:index];
				// If word character, append and advance
				if ([self isWordCharacter:character]) {
					[word appendFormat:@"%C", character];
				} else {
					inword = NO;
				}
				index = index + 1;
				// End it if we're at the document end
				if (index == maxindex) {
					inword = NO;
				}
			}
		} else {
			// Although we haven't advanced any, lastindex logic assumes we've
			// been incrementing as we go, so bump it up one to compensate
			index = index + 1;
		}
	}
	// Set the last index of the word
	if (index <= maxindex) {
		lastindex = index - 1;
	} else {
		lastindex = index;
	}
	// Ready to go backward, so reset index to one less than cursor location
	index = cursor - 1;
	// Only walk backwards if we aren't at the beginning of the document
	if (index >= 0) {
		inword = YES;
		while (inword) {
			character = [[context string] characterAtIndex:index];
			if ([self isWordCharacter:character] && ![self lineToIndexEndsWithTag:index inContext:context]) {
				[word insertString:[NSString stringWithFormat:@"%C", character] atIndex:0];
				index = index - 1;
			} else {
				inword = NO;
			}
			if (index < 0) {
				inword = NO;
			}
		}
	}
	// Since index is left-aligned and we've overcompensated, need to increment +1
	firstindex = index + 1;
	// Switch last index to length for use in range
    lastindex = lastindex - firstindex;
	*range = NSMakeRange(firstindex, lastindex);
	return [NSString stringWithString:word];
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
	NSString *e_tab_size = [NSString stringWithFormat:@"%lu", (unsigned long)[prefs numberOfSpacesForTab]];
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
	NSString *outString = nil;
	
	NSString *file = [self findScript:[self script]];
	if (file == nil) {
		NSLog(@"Error: TEALoader could not find script");
		return NO;
	}
	
	// Make sure the script is executable
	NSFileManager *fileManager = [NSFileManager defaultManager];
	if (![fileManager isExecutableFileAtPath:file]) {
		NSArray *chmodArguments = [NSArray arrayWithObjects:@"775", file, nil];
		NSTask *chmod = [NSTask launchedTaskWithLaunchPath:@"/bin/chmod" arguments:chmodArguments];
		[chmod waitUntilExit];
	}
	
	// Loop over the ranges and perform the script's action on each
	// Looping allows us to handle single ranges or multiple discontiguous selections
	for (NSValue *rangeValue in ranges) {
		NSRange range = [rangeValue rangeValue];
		// Add the items that change for each range
		[self addObject:[[context string] substringWithRange:range] forKey:@"E_SELECTED_TEXT" toDictionary:env];
		// Determine the current word
		NSRange word_range;
		NSString *current_word = [self getWordAtIndex:range.location inContext:context forRange:&word_range];
		[self addObject:current_word forKey:@"E_CURRENT_WORD" toDictionary:env];
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
		NSString *source = @"input";
		NSString *inputStr;
		if ([[self input] isEqualToString:@"selection"]) {
			inputStr = [[context string] substringWithRange:range];
			if ([inputStr isEqualToString:@""]) {
				if ([[self alternate] isEqualToString:@"document"]) {
					// Use the document's context as the input
					inputStr = [context string];
				} else if ([[self alternate] isEqualToString:@"line"]) {
					// Use the current line's content as the input
					NSRange linerange = [[context lineStorage] lineRangeForIndex:range.location];
					// Discard the linebreak at the end of the line
					range = NSMakeRange(linerange.location, linerange.length - 1);
					inputStr = [[context string] substringWithRange:range];
				} else if ([[self alternate] isEqualToString:@"word"]) {
					// Use the current word as the input
					range = word_range;
					inputStr = current_word;
				} else if ([[self alternate] isEqualToString:@"character"]) {
					// Use the current character as the input if possible
					if (range.location > 0) {
						range = NSMakeRange(range.location - 1, 1);
						inputStr = [[context string] substringWithRange:range];
					}
				}
				// Set our source appropriately
				source = @"alt";
			}
		} else if ([[self input] isEqualToString:@"document"]) {
			inputStr = [context string];
		} else {
			inputStr = @"";
		}
		
		// Run the actual script
		NSTask *task = [[NSTask alloc] init];
		NSPipe *inPipe = [NSPipe pipe], *outPipe = [NSPipe pipe];
		
		// Set up the STDIN
		// TODO: grab the encoding from the Espresso API?
		NSFileHandle *fh = [inPipe fileHandleForWriting];  
		[fh writeData:[inputStr dataUsingEncoding:NSUTF8StringEncoding]];  
		[fh closeFile];
		
		[task setLaunchPath:file];
		[task setStandardOutput:outPipe];
		[task setStandardError:outPipe];
		[task setStandardInput:inPipe];
		[task setEnvironment:env];
		
		[task launch];
		
		NSData *data;
		data = [[outPipe fileHandleForReading] readDataToEndOfFile];
		outString = [[[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding] autorelease];
		
		[task waitUntilExit];
		[task release];
		
		// Insert the output
		if ([[self output] isEqualToString:@"document"] || ([source isEqualToString:@"alt"] && [[self alternate] isEqualToString:@"document"])) {
			// Replace the document
			NSRange docrange = NSMakeRange(0, [[context string] length]);
			[recipe addReplacementString:outString forRange:docrange];
			// Since we replaced the document, jump out of the loop in case there are other ranges
			break;
		} else if ([[self output] isEqualToString:@"text"]) {
			[recipe addReplacementString:outString forRange:range];
		} else if ([[self output] isEqualToString:@"snippet"]) {
			[recipe addDeletedRange:range];
			// We can only insert a single snippet, so break out of the loop
			break;
		}
	}
	
	if ([self output] == nil) {
		// If we don't have an output specified, no need to go further
		return YES;
	}
	
	// Apply the recipe
	if ([self undo_name] != nil) {
		[recipe setUndoActionName:[self undo_name]];
	}
	[recipe prepare];
	BOOL response = YES;
	if ([recipe numberOfChanges] > 0) {
		response = [context applyTextRecipe:recipe];
	}
	if ([[self output] isEqualToString:@"snippet"]) {
		// Grab the XHTML close string
		NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
		BOOL useXHTML = [defaults boolForKey:@"TEADefaultToXHTML"];
		NSString *xhtmlStr;
		if (!useXHTML) {
			xhtmlStr = @"";
		} else {
			xhtmlStr = [defaults stringForKey:@"TEASelfClosingString"];
		}
		// Replace the $E_XHTML placeholder if it exists
		NSMutableString *snippetStr = [[outString mutableCopy] autorelease];
		[snippetStr replaceOccurrencesOfString:@"$E_XHTML" withString:xhtmlStr];
		// Convert to snippet
		CETextSnippet *snippet = [CETextSnippet snippetWithString:snippetStr];
		// Insert that sucker!
		response = [context insertTextSnippet:snippet];
	}
	return response;
}

// Easier way to add empty strings to the environment dictionary
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
