'''
module for util functions
'''
import sys, re
from termcolor import colored

def error(msg, e=None):
	if msg:
		if e:
			print('{}\n{}'.format(colored(e, 'red'), msg))
		else:
			print(msg)
	sys.exit(1)

class Log:
	vars = []


class Command(Log):
	cmds = {
		'show': lambda s: print(s)
	}

	def __init__(self, cmd, arg):
		self.cmd = cmd
		self.arg = arg

	def __call__(self):
		return Command.cmds[self.cmd](self.arg)

	def __repr__(self):
		return '${} : {}'.format(self.cmd, self.arg)


class Variable(Log):
	def __init__(self, name, value):
		self.name = name
		self.value = value
		Log.vars.append(self)

	def is_defined(self):
		return self.name in [v.name for v in Log.vars]

	def __eq__(self, name):
		return self.name == name

	def __call__(self):
		Log.vars.append(self)

	def __repr__(self):
		return '{} = {}'.format(self.name, self.value)

def get_var(name):
	if name in [v.name for v in Log.vars]:
		i = Log.vars.index(name)
		return Log.vars[i]
	else:
		return None

def trim(s):
	if s.startswith('\'') and s.endswith('\''):
		return s[1:-1]
	else:
		return s


def parse(contents):
	stuff = []
	for line in contents:
		for c in Command.cmds:
			# comments
			if line.startswith('~'):
				continue

			# command (ie. show)
			if line.startswith(c):
				data = ' '.join(line.split()[1:])

				if '\'' not in data:
					'''check if the variable has been defined'''
					if data.startswith(':') and data.endswith(':'):
						data = data[1:-1]
					if data in [v.name for v in Log.vars]:
						stuff.append(Command(c, get_var(data).value))
						continue
					else:
						error('Undefined variable: {}'.format(data), e=line)

				'''string interpolation'''
				pol_regex = r':(\w+):'
				s = re.search(pol_regex, data)
				if s:
					var_name = s.group(1)
					var = get_var(var_name)
					if var:
						s = data[:s.start()] + var.value + data[s.end():]
						s = trim(s)
						stuff.append(Command(c, s))
						continue
					else:
						error('Undefined variable: {}'.format(data), e=line)

				msg_regex = r'\'?([-\w\d ,!.;?]*)\'?'
				string = re.search(msg_regex, data).group(1)
				stuff.append(Command(c, string))

			# variable assignment
			elif line.split()[1] == 'is:':
				data = line.split()
				data.pop(1)
				if len(data) > 2: error('Too many values in assignment.', e=line)
				var, value = data[0], trim(data[1])
				stuff.append(Variable(var, value))

			else:
				error('Not a real command.', e=line)

	return stuff
