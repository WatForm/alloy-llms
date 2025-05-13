import os
import sys
import json
import subprocess

def download(url,folder):
	global config
	command = config["download_command"]+" \""+url+"\""+" -o "+"\""+folder+"\""
	print(command)
	os.system(command)