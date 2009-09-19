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

@interface TEAForEspresso : TEAGenericAction {
	// TEAforEspresso properties
	NSString *action;
	NSDictionary *options;
}

@property (readonly,copy) NSString* action;
@property (readonly,retain) NSDictionary* options;

@end
