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

/*
  We face a dilemma: how to pass a Python function an Objective-C object (context) along with
  an NSDictionary, and receive a return value in turn?
  
  Using the Python C API turned out to be far more complicated than I wanted, so instead
  I opted to abstract the actual loading functionality out to a class in Python.
  
  This allows us to easily use the PyObjC bridge to pass info from the Objective-C class to Python.
*/

// This forward-declares the methods in TEAPythonLoader to avoid compile errors
@class TEAPythonLoader;

@interface NSObject (MethodsThatReallyDoExist)
- (BOOL)actInContext:(id)context withOptions:(NSDictionary *)options forAction:(id)actionObject;
@end

// This allows us to create private setters for these variables
// I was having mad memory leaks until I switched solely to using properties; probably a better way out there, though
@interface TEAforEspresso ()
@property (readwrite,copy) NSString* action;
@property (readwrite,retain) NSDictionary* options;
@end

// The actual implementation of the class
@implementation TEAforEspresso

@synthesize action;
@synthesize options;

- (id)initWithDictionary:(NSDictionary *)dictionary bundlePath:(NSString *)myBundlePath {
	self = [super initWithDictionary:dictionary bundlePath:myBundlePath];
	if (self == nil)
		return nil;
	
	// Grab the target action
	if ([dictionary objectForKey:@"target_action"] != nil) {
		[self setAction:[dictionary objectForKey:@"target_action"]];
	} else {
		[self setAction:[dictionary objectForKey:@"action"]];
	}
	
	// Grab the list of options
	if ([dictionary objectForKey:@"arguments"] != nil) {
		[self setOptions:[dictionary objectForKey:@"argument"]];
	} else {
		[self setOptions:[dictionary objectForKey:@"options"]];
	}
	
	// ONE-TIME INITIALIZATION ITEMS NEED TO GO HERE TO GENERATE SYMLINKS
	
	return self;
}

- (BOOL)performActionWithContext:(id)context error:(NSError **)outError {
	// Make sure we have an action defined
	if ([self action] == nil) {
		NSLog(@"TEA Error: Missing action tag in XML");
		return NO;
	}
	
	if (!Py_IsInitialized()) {
		// Construct the Python search paths
		NSMutableArray *pythonPathArray = [NSMutableArray array];
		for (NSString *path in [self supportPaths]) {
			[pythonPathArray addObject:[path stringByAppendingPathComponent:@"Library"]];
		}
		setenv("PYTHONPATH", [[pythonPathArray componentsJoinedByString:@":"] UTF8String], 1);
		
		// Initialize the Python interpreter
		Py_SetProgramName("/usr/bin/env python");
		Py_Initialize();
		
		// Execute the Python loader class file to make sure it's in memory
		// This stuff is straight out of the Python app Xcode template
		NSString *mainPath = [[self teaPath] stringByAppendingPathComponent:@"Support/Library/TEAPythonLoader.py"];
		
		const char *mainPathPtr = [mainPath UTF8String];
		FILE *mainFile = fopen(mainPathPtr, "r");
		int result = PyRun_SimpleFile(mainFile, (char *)[[mainPath lastPathComponent] UTF8String]);
		if ( result != 0 )
			[NSException raise: NSInternalInconsistencyException
						format: @"%s:%d main() PyRun_SimpleFile failed with file '%@'.  See console for errors.", __FILE__, __LINE__, mainPath];
	}
	
	// Now that Python and the TEAPythonLoader class are initialized, send the info to TEAPythonLoader
	Class TEAPythonLoaderClass = NSClassFromString(@"TEAPythonLoader");
	id actionLoader = [[TEAPythonLoaderClass alloc] init];
	BOOL actionResult = [actionLoader actInContext:context withOptions:[self options] forAction:self];
	
	return actionResult;	
}

@end
