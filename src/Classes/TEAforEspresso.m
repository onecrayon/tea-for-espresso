//
//  TEAforEspresso.m
//  TEA for Espresso.sugar
//
//  Created by Ian Beck
//  http://onecrayon.com/tea/
//
//  MIT License

#import <Python/Python.h>
#import "TEAforEspresso.h"

// This allows us to create private setters for these variables
// I was having mad memory leaks until I switched solely to using properties; probably a better way out there, though
@interface TEAforEspresso ()
@property (readwrite,copy) NSString* action;
@property (readwrite,retain) NSDictionary* options;
@property (readwrite) BOOL passActionObject;

- (void) execTEALoaderClass;
@end

// It's possible the Python interpreter was setup by another plugin compiled with PyObjc (bash.sugar, for instance)
// If this was the case, we have to check to see if we've run basic init code, and do it even if we aren't starting the interpreter
static BOOL TEAinitPythonComplete = NO;

// The actual implementation of the class
@implementation TEAforEspresso

@synthesize action;
@synthesize options;
@synthesize passActionObject;

- (id)initWithDictionary:(NSDictionary *)dictionary bundlePath:(NSString *)myBundlePath {
	self = [super initWithDictionary:dictionary bundlePath:myBundlePath];
	if (self == nil)
		return nil;
	
	// Grab the target action
	NSString *targetAction = [dictionary objectForKey:@"target_action"];
	if (targetAction != nil) {
		[self setAction:targetAction];
	} else {
		[self setAction:[dictionary objectForKey:@"action"]];
	}
	
	// Grab the list of options
	NSDictionary *arguments = [dictionary objectForKey:@"arguments"];
	if (arguments != nil) {
		[self setOptions:arguments];
	} else {
		[self setOptions:[dictionary objectForKey:@"options"]];
	}
	
	// Check to see if we should be passing our action object along
	// NOTE: objectForKey returns nil if pass_action_object is not defined and methods sent to nil always return NO
	[self setPassActionObject:[[dictionary objectForKey:@"pass_action_object"] caseInsensitiveCompare:@"true"]];
	
	return self;
}

- (void)dealloc
{
	[self setAction:nil];
	[self setOptions:nil];
	[super dealloc];
}

- (BOOL)performActionWithContext:(id)context error:(NSError **)outError {
	// Make sure we have an action defined
	if ([self action] == nil) {
		NSLog(@"TEA Error: Missing action tag in XML");
		return NO;
	}
	
	[self initPython];
	
	// Now that Python and the TEAPythonLoader class are initialized, send the info to TEAPythonLoader
	Class TEAPythonLoaderClass = NSClassFromString(@"TEAPythonLoader");
	id actionLoader = [[[TEAPythonLoaderClass alloc] init] autorelease];
	return [actionLoader actInContext:context forAction:self];
}

- (void) initPython {
	if (!Py_IsInitialized()) {
		// Construct the Python search paths
		NSMutableArray *pythonPathArray = [NSMutableArray array];
		for (NSString *path in [self supportPaths]) {
			[pythonPathArray addObject:[path stringByAppendingPathComponent:@"Library"]];
		}
		setenv("PYTHONPATH", [[pythonPathArray componentsJoinedByString:@":"] UTF8String], 1);
		
		// Initialize the Python interpreter
		Py_SetProgramName("/usr/bin/python");
		Py_Initialize();
		
		[self execTEALoaderClass];
	} else if (!TEAinitPythonComplete) {
		[self execTEALoaderClass];
	}
}

- (void) execTEALoaderClass {
	// Execute the Python loader class file to make sure it's in memory
	// This stuff is straight out of the Python app Xcode template
	NSString *mainPath = [[self teaPath] stringByAppendingPathComponent:@"Support/Library/TEAPythonLoader.py"];
	
	const char *mainPathPtr = [mainPath UTF8String];
	FILE *mainFile = fopen(mainPathPtr, "r");
	if (mainFile == NULL)
		return;
	
	int result = PyRun_SimpleFile(mainFile, (char *)[[mainPath lastPathComponent] UTF8String]);
	fclose(mainFile);
	if ( result != 0 )
		[NSException raise: NSInternalInconsistencyException
					format: @"%s:%lu main() PyRun_SimpleFile failed with file '%@'.  See console for errors.", __FILE__, (unsigned long)__LINE__, mainPath];
	else
		TEAinitPythonComplete = YES;
}

@end
