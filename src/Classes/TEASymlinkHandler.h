//
//  TEASymlinkHandler.h
//  TEA for Espresso.sugar
//
//  Created by Ian Beck
//  http://onecrayon.com/tea/
//
//  MIT License
//

#import <Cocoa/Cocoa.h>


@interface TEASymlinkHandler : NSObject {

}

-(void)rebuild;
-(void)refresh;
-(void)parseSupportFolders;
-(BOOL)symlink:(NSString *)link isValidForPath:(NSString *)path;
-(BOOL)customActionsEnabled;

@end
