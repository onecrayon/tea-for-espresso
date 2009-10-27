//
//  TEALoader.h
//  TEA for Espresso.sugar
//
//  Created by Ian Beck
//  http://onecrayon.com/tea/
//
//  MIT License

#import <Cocoa/Cocoa.h>
#import "TEAGenericAction.h"


@interface TEALoader : TEAGenericAction {
	NSString* script;
	NSString* input;
	NSString* alt;
	NSString* output;
	NSString* undo;
}

@property (readonly,copy) NSString* script;
@property (readonly,copy) NSString* input;
@property (readonly,copy) NSString* alt;
@property (readonly,copy) NSString* output;
@property (readonly,copy) NSString* undo;

- (BOOL)addObject:(id)myObject forKey:(id)myKey toDictionary:(NSMutableDictionary*)dictionary;

@end
