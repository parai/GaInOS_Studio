from distutils.core import setup
import py2exe

py2exe_options = {
        "includes":["sip",],
        }

setup(windows=["GaInOS_Studio.py"], options={'py2exe':py2exe_options})