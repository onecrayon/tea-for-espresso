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
	
	// Set up the environment variables that don't change
	NSDictionary *baseEnv = [NSDictionary dictionaryWithObjectsAndKeys:
								[self bundlePath], @"E_SUGARPATH"
							 ];
}

@end
