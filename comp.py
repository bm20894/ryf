#!/usr/bin/env python3

'''
Interpret .ryf file
'''
import sys, utils

try:
	filepath = sys.argv[1]
	if not filepath.endswith('.ryf'):
		utils.error('Incorrect file extension. must be a .ryf file.')
except IndexError:
	'''Maybe go into interperter??'''
	utils.error('No file specified.')

def get_cmds(filepath):
	try:
		with open(filepath, 'r') as f:
			contents = f.readlines()
	except:
		utils.error('That is not a real file!')
	else:
		contents = [c for c in [line.strip() for line in contents] if len(c) > 0]
		'''parse data in file'''
		return utils.parse(contents)


cmds = get_cmds(filepath)

for cmd in cmds:
	cmd()