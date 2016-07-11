This script creates Mac OS X apps and dmgs from Anaconda Python environments. Anaconda environments are already isolated from the rest of the system, as in, all dependencies of conda packages are contained in the environment itself and no packages outside of the environment should be required. This makes an Anaconda environment distributable 'as is'. It just needs to be packaged as an app. That's what this script does.

The benefit of doing it like this instead of using py2app is:

- The process is much more transparent, basically your app will be a direct copy of the
Anaconda environment with no things changed, and all steps can be followed or changed in the script.
- The resulting app will not be frozen. This makes it easier to maintain or (auto) update it.
- Best of all, multiprocessing (in combination with billiard and spawn) will work in Python 2. I didn't get this to happen with billiard+py2app.

## Dependencies
- biplist
- six
- dmgbuild

## Usage
Create a python script as a configuration file, and pass it as a command line argument to conda_env_to_app, e.g.:

    ./conda_env_to_app settings.py

This settings file should specify all the necessary variables that are required to generate the app (and the dmg if desired). See the included settings.py as an example. This settings file was created to package the [OpenSesame experiment builder](http://github.com/smathot/OpenSesame).