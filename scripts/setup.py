"""
Sets up Alloy .jar files in ./tools, no arguments required. Downloads from links in conf.json, saves using names in conf.json
"""
from lib import *



download(config["Alloy_6"]["link"],"./tools/"+config["Alloy_6"]["jar"])
download(config["Alloy_5"]["link"],"./tools/"+config["Alloy_5"]["jar"])


