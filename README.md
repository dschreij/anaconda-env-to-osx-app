This script creates Mac OS X apps and dmgs from Anaconda Python environments. 
The benefit of doing this instead of using py2app is:

- The process is much more transparent, basically your app will be a direct copy of the
Anaconda environment with no things changed, and all othe steps can be followed in the script.
- The resulting app will not be frozen. This makes it easier to maintain or (auto)update it 
- Best of all, multiprocessing (in combination with billiard and spawn) will work in Python 2.

## Dependencies
- biplist
- six
- dmgbuild
