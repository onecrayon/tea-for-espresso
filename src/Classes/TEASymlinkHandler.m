//
//  TEASymlinkHandler.h
//  TEA for Espresso.sugar
//
//  Created by Ian Beck
//  http://onecrayon.com/tea/
//
//  MIT License
//

#import "TEASymlinkHandler.h"


@implementation TEASymlinkHandler

// If enabled, add new files, otherwise remove all symlinks
-(void)rebuild {
	if ([self customActionsEnabled]) {
		[self parseSupportFolders];
	} else {
		// Remove all symlinks
		NSBundle *bundle = [NSBundle bundleWithIdentifier:@"com.onecrayon.tea.espresso"];
		NSString *symFolder = [[bundle bundlePath] stringByAppendingPathComponent:@"TextActions"];
		// TODO: loop over all files, check if symlink and destroy if so
	}

}

// If enabled, run our standard check for new files
-(void)refresh {
	if ([self customActionsEnabled]) {
		[self parseSupportFolders];
	}
}

// Walk over the support folder and look for new files
-(void)parseSupportFolders {
	NSBundle *bundle = [NSBundle bundleWithIdentifier:@"com.onecrayon.tea.espresso"];
	NSString *symFolder = [[bundle bundlePath] stringByAppendingPathComponent:@"TextActions"];
	// For backwards compatibility with early TEA versions, I need to support the TEA folder
	NSArray *paths = [NSArray arrayWithObjects:[@"~/Library/Application Support/Espresso/Support/TextActions/" stringByExpandingTildeInPath],
					  [@"~/Library/Application Support/Espresso/TEA/TextActions/" stringByExpandingTildeInPath], nil];
	NSFileManager *fileManager = [NSFileManager defaultManager];
	// Process both folders
	for (NSString *directory in paths) {
		NSDirectoryEnumerator *dirEnumerator = [fileManager enumeratorAtPath:directory];
		
		NSString *file;
		while ((file = [dirEnumerator nextObject])) {
			if ([[file pathExtension] isEqualToString:@"xml"]) {
				// Create an autorelease pool so we can reinstantiate all these variables each loop
				NSAutoreleasePool *pool = [NSAutoreleasePool new];
				
				NSString *basename = [file lastPathComponent];
				// This stuff changes in the next while loop
				NSString *fileStub = [basename copy];
				BOOL priorLink = NO;
				NSUInteger count = 1;
				while ([fileManager fileExistsAtPath:[symFolder stringByAppendingPathComponent:fileStub]]) {
					// If we already have a link, set priorLink to YES and break
					if ([self symlink:[symFolder stringByAppendingPathComponent:fileStub] isValidForPath:file]) {
						priorLink = YES;
						break;
					} else {
						// Otherwise, bump our number up and try again
						[fileStub release];
						fileStub = [[NSString stringWithFormat:@"%d", count] stringByAppendingString:basename];
						count = count + 1;
					}
				}
				if (!priorLink) {
					[fileManager createSymbolicLinkAtPath:[symFolder stringByAppendingString:fileStub] withDestinationPath:file error:NULL];
				}
				// Release the pool
				[pool drain];
			}
		}
	}
}

-(BOOL)symlink:(NSString *)link isValidForPath:(NSString *)path {
	NSFileManager *fileManager = [NSFileManager defaultManager];
	return ([[[fileManager attributesOfItemAtPath:link error:NULL] fileType] isEqualToString:NSFileTypeSymbolicLink] && [[fileManager destinationOfSymbolicLinkAtPath:link error:NULL] isEqualToString:path]);
}

// Test if custom actions are enabled at this time
-(BOOL)customActionsEnabled {
	NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
	return [defaults boolForKey:@"TEAEnableUserActions"];
}

@end
