"""
Designed to see if code is valid Alloy code, along with version
Uses one argument for file path
"""

from lib import *

def check_validity(file_path):
	valid = {"passes_5":False,"passes_6":False}
	command6 = ALLOY_6_COMMANDS+" "+file_path
	command5 = ALLOY_5_COMMANDS+" "+file_path
	result_6 = execute(command6)
	valid["passes_6"] = len(result_6.stderr)==0
	return valid


if __name__ == "__main__":
	print(check_validity(sys.argv[1]))