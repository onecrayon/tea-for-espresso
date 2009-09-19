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

// This allows us to set private setters for these variables
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
		
		Py_SetProgramName("/usr/bin/python");
		Py_Initialize();
//		PySys_SetArgv(argc, (char **)argv);
	}
	
	// Find the action module
	NSString *actionPath = [self findScript:[self action]];
	if (actionPath == nil) {
		NSLog(@"TEA Error: Could not find Python module %s", actionPath);
		return NO;
	}
	
	// NEED TO FIGURE OUT:
	// - How to call a specific Python function
	// - How to pass keyword arguments to the Python function
	// - How to parse the Python function's return value as a bool
	
	/*
	 You may also call a function with keyword arguments by using PyObject_Call(), which supports arguments and keyword arguments.
	 As in the above example, we use Py_BuildValue() to construct the dictionary.
	 
		PyObject *dict;
		...
		dict = Py_BuildValue("{s:i}", "name", val);
		result = PyObject_Call(my_callback, NULL, dict);
		Py_DECREF(dict);
		if (result == NULL)
		return NULL; // Pass error back
		// Here maybe use the result
		Py_DECREF(result);
	 
	 http://docs.python.org/extending/extending.html
	 
	 Use PyDict_New() and similar to construct the dictionary instead? Not sure how to convert from NSDictionary
	*/
	
}

@end
