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
		NSLog(@"Parsing folders");
		[self parseSupportFolders];
	} else {
		// Remove all symlinks
		NSBundle *bundle = [NSBundle bundleWithIdentifier:@"com.onecrayon.tea.espresso"];
		NSString *symFolder = [[bundle bundlePath] stringByAppendingPathComponent:@"TextActions"];
		NSFileManager *fileManager = [NSFileManager defaultManager];
		// Grab the contents of the TextActions folder
		NSArray *contents = [fileManager contentsOfDirectoryAtPath:symFolder error:NULL];
		// Process the symlinks
		for (NSString *path in contents) {
			NSLog(@"Working on path: %@", [symFolder stringByAppendingPathComponent:path]);
			if ([[[fileManager attributesOfItemAtPath:[symFolder stringByAppendingPathComponent:path] error:NULL] fileType] isEqualToString:NSFileTypeSymbolicLink]) {
				NSError *error = nil;
				if (![fileManager removeItemAtPath:[symFolder stringByAppendingPathComponent:path] error:&error]) {
					NSLog(@"Error removing symlink: %@ for %@", [error localizedDescription], path);
				}
			}
		}
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
		BOOL keepRunning = YES;
		// Using keepRunning instead of standard iterator setup to prevent autorelease memory problem:
		// http://www.cocoadev.com/index.pl?NSDirectoryEnumerator (near the bottom)
		while (keepRunning) {
			file = [dirEnumerator nextObject];
			if (file == nil) {
				keepRunning = NO;
				break;
			}
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
						fileStub = [[NSString stringWithFormat:@"%lu", (unsigned long)count] stringByAppendingString:basename];
						count = count + 1;
					}
				}
				if (!priorLink) {
					NSError *error = nil;
					if (![fileManager createSymbolicLinkAtPath:[symFolder stringByAppendingPathComponent:fileStub] withDestinationPath:[directory stringByAppendingPathComponent:file] error:&error]) {
						NSLog(@"Error creating symlink: %@ for %@ => %@", [error localizedDescription], [symFolder stringByAppendingPathComponent:fileStub], [directory stringByAppendingPathComponent:file]);
					}
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
	NSLog(@"TEAEnableUserActions: %d", [defaults boolForKey:@"TEAEnableUserActions"]);
	return [defaults boolForKey:@"TEAEnableUserActions"];
}

@end
