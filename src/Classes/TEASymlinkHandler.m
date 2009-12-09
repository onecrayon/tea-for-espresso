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

- (NSBundle *)TEABundle
{
	return [NSBundle bundleWithIdentifier:@"com.onecrayon.tea.espresso"];
}

+ (void)load
{
	[super load];
	
	// This is really a bit of a hacky way to approach this, but it works...
	// Runs one-time initialization code upon bundle load
	NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];
	// Setup the default preferences, in case they've never been modified
	NSString *defaults = [[[self sharedHandler] TEABundle] pathForResource:@"Defaults" ofType:@"plist"];
	if (defaults != nil) {
		[[NSUserDefaults standardUserDefaults] registerDefaults:[NSDictionary dictionaryWithContentsOfFile:defaults]];
	}
	// Refresh the symlinks to make sure they're accurate
	[[self sharedHandler] refresh];
	[pool drain];
}

+ (TEASymlinkHandler *)sharedHandler
{
	static TEASymlinkHandler *sharedHandler = nil;
	if (sharedHandler == nil)
		sharedHandler = [[self alloc] init];
	return sharedHandler;
}

// Test if custom actions are enabled at this time
- (BOOL)hasCustomActionsEnabled
{
	return [[NSUserDefaults standardUserDefaults] boolForKey:@"TEAEnableUserActions"];
}

// Walk over the support folder and look for new files
- (void)parseSupportFolders
{
	NSString *symbolicLinksFolder = [[[self TEABundle] bundlePath] stringByAppendingPathComponent:@"TextActions"];
	
	// For backwards compatibility with early TEA versions, I need to support the TEA folder
	NSArray *directoriesWithXML = [NSArray arrayWithObjects:[@"~/Library/Application Support/Espresso/Support/TextActions/" stringByExpandingTildeInPath], [@"~/Library/Application Support/Espresso/TEA/TextActions/" stringByExpandingTildeInPath], nil];
	NSFileManager *fileManager = [NSFileManager defaultManager];
	
	// Process both folders
	for (NSString *directoryWithXML in directoriesWithXML) {
		
		NSArray *subpaths = [fileManager subpathsOfDirectoryAtPath:directoryWithXML error:NULL];
		for (NSString *subpath in subpaths) {
			
			// If we found an XML file, we add a symlink to it
			if ([subpath.pathExtension isEqualToString:@"xml"]) {
				
				NSString *fileName = [subpath lastPathComponent];
				NSString *filePath = [directoryWithXML stringByAppendingPathComponent:subpath];
				
				BOOL hasValidSymbolicLink = NO;
				NSUInteger numericPrefix = 1;
				while ([fileManager fileExistsAtPath:[symbolicLinksFolder stringByAppendingPathComponent:fileName]]) {
					
					// See if we already have a valid symbolic link for the file we want to point to
					NSString *symbolicLinkPath = [symbolicLinksFolder stringByAppendingPathComponent:fileName];
					hasValidSymbolicLink = ([[[fileManager attributesOfItemAtPath:symbolicLinkPath error:NULL] fileType] isEqualToString:NSFileTypeSymbolicLink] && [[fileManager destinationOfSymbolicLinkAtPath:symbolicLinkPath error:NULL] isEqualToString:filePath]);
					
					if (hasValidSymbolicLink) {
						break;
					}
					else {
						fileName = [NSString stringWithFormat:@"%lu-%@", (unsigned long)numericPrefix, fileName];
						numericPrefix++;
					}
				}
				
				if (!hasValidSymbolicLink) {
					NSError *error = nil;
					if (![fileManager createSymbolicLinkAtPath:[symbolicLinksFolder stringByAppendingPathComponent:fileName] withDestinationPath:filePath error:&error]) {
						NSLog(@"TEA: Error creating symlink: %@ for %@ => %@", [error localizedDescription], [symbolicLinksFolder stringByAppendingPathComponent:fileName], filePath);
					}
				}
			}
		}
	}
}

#pragma mark -

// If enabled, add new files, otherwise remove all symlinks
- (void)rebuild
{
	if ([self hasCustomActionsEnabled]) {
		[self parseSupportFolders];
	}
	else {
		// Remove all symlinks
		NSString *symFolder = [[[self TEABundle] bundlePath] stringByAppendingPathComponent:@"TextActions"];
		
		// Process the symlinks
		NSFileManager *fileManager = [NSFileManager defaultManager];
		for (NSString *path in [fileManager contentsOfDirectoryAtPath:symFolder error:NULL]) {
			
			NSString *symbolicLinkPath = [symFolder stringByAppendingPathComponent:path];
			if ([[[fileManager attributesOfItemAtPath:symbolicLinkPath error:NULL] fileType] isEqualToString:NSFileTypeSymbolicLink]) {
				NSError *error = nil;
				if (![fileManager removeItemAtPath:symbolicLinkPath error:&error]) {
					NSLog(@"Error removing symlink: %@ for %@", [error localizedDescription], path);
				}
			}
		}
	}
	
}

// If enabled, run our standard check for new files
- (void)refresh
{
	if ([self hasCustomActionsEnabled]) {
		[self parseSupportFolders];
	}
}

@end
