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
	NSString* alternate;
	NSString* output;
	NSString* undo_name;
}

@property (readonly,copy) NSString* script;
@property (readonly,copy) NSString* input;
@property (readonly,copy) NSString* alternate;
@property (readonly,copy) NSString* output;
@property (readonly,copy) NSString* undo_name;

- (BOOL)addObject:(id)myObject forKey:(NSString *)myKey toDictionary:(NSMutableDictionary*)dictionary;

@end
