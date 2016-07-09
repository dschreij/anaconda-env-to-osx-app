# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from AppKit import NSScreen
frame = NSScreen.mainScreen().frame()
xres = frame.size.width
yres = frame.size.height

APP_NAME = "OpenSesame"
VERSION = "3.1.0"
IDENTIFIER = "nl.cogsci.osdoc"
APP_EXT = "osexp"
AUTHOR = "Sebastiaan Mathot",
CONDA_ENV_PATH = "/Users/daniel/anaconda/envs/OpenSesame"
CONDA_FOLDERS = ["lib", "bin", "share", "conda-meta", "qsci", "ssl", "translations"]
ICON_PATH = "/Users/daniel/Github/OpenSesame/opensesame_resources/opensesame.icns"
ENTRY_SCRIPT = "opensesame"
LOCAL_LIB_FOLDER = "/usr/local/lib"
OUTPUT_FOLDER = "~/EXPERIMENTAL/"
CFBUNDLETYPEROLE = "Editor"
LSItemContentTypes = "public.item"

# ===== Settings specific to dmgbuild =====

DMG_FILE = 'opensesame_{}-py2.7-macos-1.dmg'.format(VERSION)
DMG_FORMAT = 'UDBZ'
DMG_BACKGROUND = "/Users/daniel/Github/OpenSesame/opensesame_resources/einstein.png"
DMG_ICON_LOCATIONS = {
	APP_NAME + '.app': (30, 450),
	'Applications' : (300, 450)
}

# Center the window
win_size = (358, 570)
x_win = xres/2 - win_size[0]/2
y_win = yres/2 - win_size[1]/2

DMG_WINDOW = ((x_win, y_win), win_size)
DMG_ICON_SIZE = 80
