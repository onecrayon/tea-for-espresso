//
//  TEAGenericAction.h
//  TEA for Espresso.sugar
//
//  Created by Ian Beck
//  http://onecrayon.com/tea/
//
//  MIT License
//

#import <Cocoa/Cocoa.h>

@interface TEAGenericAction : NSObject {
	// Syntax context the action can be performed in
	NSString *syntaxContext;
	// Selection context the action can be performed in
	NSString *selectionContext;
	// Bundle path is useful for finding scripts in multiple locations
	NSString *bundlePath;
	// We might not be in TEA, so track the TEA path
	NSString *teaPath
	// This tracks the locations of Support folders we need to search
	NSArray *supportPaths;
}

// Read-only properties
@property (readonly,copy) NSString* syntaxContext;
@property (readonly,copy) NSString* selectionContext;
@property (readonly,copy) NSString* bundlePath;
@property (readonly,copy) NSString* teaPath;
@property (readonly,retain) NSArray* supportPaths;

// File locating methods
- (NSString *)findScript:(NSString *)fileName inFolders:(NSArray *)folders;
- (NSString *)findScript:(NSString *)fileName;

@end
