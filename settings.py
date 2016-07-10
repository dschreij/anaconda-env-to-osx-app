# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import osxrelocator
import os
import re

#===============================================================================
# General settings applicable to all apps
#===============================================================================

# Name of the app
APP_NAME = "OpenSesame"
# The short version string
VERSION = "3.1.0"
# The website in reversered order (domain first, etc.)
IDENTIFIER = "nl.cogsci.osdoc"
# The author of this package
AUTHOR = "Sebastiaan Mathot"
# Path to the anaconda environment folder to package
CONDA_ENV_PATH = "~/anaconda/envs/OpenSesame"
# Folders to include from Anaconda environment, if ommitted everything will be
# copied
CONDA_FOLDERS = ["lib", "bin", "share", "qsci", "ssl", "translations"]
# Paths of files and folders to remove from the copied anaconda environment, 
# relative to the environment's root. 
# For instance, this could be the qt4 apps (an app inside an app is useless)
CONDA_EXCLUDE_FILES = [
	'bin/*-qt4*'
]
# Path to the icon of the app
ICON_PATH = "~/Github/OpenSesame/opensesame_resources/opensesame.icns"
# The entry script of the application in the environment's bin folder
ENTRY_SCRIPT = "opensesame"
# Folder to place created APP and DMG in.
OUTPUT_FOLDER = "~/EXPERIMENTAL/"
# Obligatory Info.plist setting, see:
# https://developer.apple.com/library/ios/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html
# Should be one of {Editor, Viewer, Shell, None}
CFBUNDLETYPEROLE = "Editor"

# Information about file types that the app can handle
APP_SUPPORTED_FILES = [{
	'CFBundleTypeExtensions': ["osexp"],
	'CFBundleTypeIconFile': os.path.basename(ICON_PATH),
	'LSItemContentTypes': ["public.item"] 
}]

# ===== Settings specific to dmgbuild =====

# Create a DMG template name, so version can be overwritten if it can be 
# determined from the OS libraries.
os_dmg_template = 'opensesame_{}-py2.7-macos-1.dmg'

# Name of the DMG file that will be created in OUTPUT_FOLDER
DMG_FILE = os_dmg_template.format(VERSION)
# DMG format
DMG_FORMAT = 'UDBZ'
# Locations of shortcuts in DMG window
DMG_ICON_LOCATIONS = {
	APP_NAME + '.app': (30, 450),
	'Applications' : (300, 450)
}
# Size of DMG window when mounted
DMG_WINDOW_RECT = ((300, 200), (358, 570))
# Size of icons in DMG
DMG_ICON_SIZE = 80

# Background of DMG file
DMG_BACKGROUND = "~/Github/OpenSesame/opensesame_resources/einstein.png"

#===============================================================================
# Extra settings and functions specific to OpenSesame (Remove for other apps)
#===============================================================================

LOCAL_LIB_FOLDER = "/usr/local/lib"

# Try to obtain OpenSesame version from OpenSesame source
os_metadata_file = os.path.expanduser(os.path.join(CONDA_ENV_PATH, 'lib', 'python2.7',
	'site-packages', 'libopensesame', 'metadata.py'))
try:
	with open(os_metadata_file, 'r') as fp:
		metadata = fp.read()
except Exception as e:
	print("Could not read OpenSesame version from metadata: {}".format(e))
else:
	version_match = re.search("(?<=__version__)\s*=\s*u'(.*)'", metadata)
	if version_match:
		VERSION = version_match.group(1)
		
	codename_match = re.search("(?<=codename)\s*=\s*u'(.*)'", metadata)
	if codename_match:
		codename = codename_match.group(1)
		LONG_VERSION = VERSION + ' ' + codename
	else:
		LONG_VERSION = VERSION

	# Overwrite name of the DMG file that will be created in OUTPUT_FOLDER
	DMG_FILE = os_dmg_template.format(VERSION)

	print("Creating app for {} {}".format(APP_NAME, LONG_VERSION))

def extra():
	copy_opensesame_with_py_ext()
	# copy_libpng()
	copy_sdl_libraries()
	correct_pygame_links()

def copy_opensesame_with_py_ext():
	""" Copy bin/opensesame to bin/opensesame.py to enable multiprocessing """
	shutil.copy(
		os.path.join(RESOURCE_DIR, 'bin', ENTRY_SCRIPT),
		os.path.join(RESOURCE_DIR, 'bin', ENTRY_SCRIPT + '.py')
	)

def copy_libpng():
	""" Copy newer (Homebrew) libpng to Resources folder, 
	as the Anaconda one is too old """
	print("Copying libpng16.16.dylib")
	try:
		shutil.copyfile('/usr/local/opt/libpng/lib/libpng16.16.dylib',
			os.path.join(RESOURCE_DIR, 'lib', 'libpng16.16.dylib'))
	except OSError as e:
		print("Error copying libpng: {}".format(e))

def copy_sdl_libraries():
	""" Copy SDL files into Resources/lib """
	print("Copying SDL library from {} to {}".format(LOCAL_LIB_FOLDER,
		os.path.join(RESOURCE_DIR, 'lib')))

	SDL_files = [
		'libSDL-1.2.0.dylib',
		'libSDL_image-1.2.0.dylib',
		'libSDL_mixer-1.2.0.dylib',
		'libSDL_ttf-2.0.0.dylib',
		'libportmidi.dylib',
		'libportaudio.2.dylib',
	]

	try:
		for SDL_lib in SDL_files:
			shutil.copy2(
				os.path.join(LOCAL_LIB_FOLDER, SDL_lib),
				os.path.join(RESOURCE_DIR, 'lib', SDL_lib),
			)
			os.chmod(os.path.join(RESOURCE_DIR, 'lib', SDL_lib), 0o755)
	except OSError as e:
		print("Could not copy SDL libraries: e".format(e))

	print("========== Correcting internal references of SDL files ==========")

	relocator = osxrelocator.OSXRelocator(
		RESOURCE_DIR + '/lib', '/usr/local/lib',
		'@rpath/', False)
	relocator.relocate()

	relocator = osxrelocator.OSXRelocator(
		RESOURCE_DIR + '/lib',
		'/usr/local/opt/sdl_image/lib/',
		'@rpath/', False)
	relocator.relocate()

	relocator = osxrelocator.OSXRelocator(
		RESOURCE_DIR + '/lib',
		'/usr/local/opt/sdl/lib/',
		'@rpath/', False)
	relocator.relocate()

def correct_pygame_links():
	""" Correct the internal links of pygame to SDL """
	print("========== Correcting pygame links to SDL ==========")
	pygame_path = os.path.join(RESOURCE_DIR, 'lib',
		'python{}.{}'.format(sys.version_info.major, sys.version_info.minor),
		'site-packages','pygame')

	relocator = osxrelocator.OSXRelocator(
		pygame_path,
		LOCAL_LIB_FOLDER,
		'@rpath/',
		False)
	relocator.relocate()

	relocator = osxrelocator.OSXRelocator(
		pygame_path,
		'/usr/local/opt/sdl_image/lib/',
		'@rpath/',
		False)
	relocator.relocate()

	relocator = osxrelocator.OSXRelocator(
		pygame_path,
		'/usr/local/opt/libpng/lib/',
		'@rpath/',
		False)
	relocator.relocate()


