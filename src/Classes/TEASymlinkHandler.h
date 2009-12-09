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

+ (TEASymlinkHandler *)sharedHandler;

- (void)rebuild;
- (void)refresh;

@end
