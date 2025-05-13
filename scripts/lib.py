"""
Used to store functions which are generally useful in many scripts
"""

import os
import sys
import json
import subprocess

with open("./conf.json") as f:
	config = json.load(f)

def download(url,folder):
	global config
	command = config["download_command"]+" \""+url+"\""+" -o "+"\""+folder+"\""
	print(command)
	os.system(command)

def get_commands_command(jarname):
	return config["java_command"]+" -jar ./tools/"+jarname+" commands"

def execute(command):
	return subprocess.run([command],text=True,shell=True,capture_output=True)

ALLOY_6_COMMANDS = get_commands_command(config["Alloy_6"]["jar"])
ALLOY_5_COMMANDS = get_commands_command(config["Alloy_5"]["jar"])

