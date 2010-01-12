//
//  TEAforEspresso.h
//  TEA for Espresso.sugar
//
//  Created by Ian Beck
//  http://onecrayon.com/tea/
//
//  MIT License

#import <Cocoa/Cocoa.h>
#import "TEAGenericAction.h"

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
- (BOOL)actInContext:(id)context forAction:(id)actionObject;
@end


// Our actual class definition
@interface TEAforEspresso : TEAGenericAction {
	// TEAforEspresso properties
	NSString *action;
	NSDictionary *options;
	BOOL passActionObject;
}

@property (readonly,copy) NSString* action;
@property (readonly,retain) NSDictionary* options;
@property (readonly) BOOL passActionObject;

- (void) initPython;

@end
