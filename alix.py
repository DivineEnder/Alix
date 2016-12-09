import sys
import os
from subprocess import call as cmd

ALIXES = os.path.realpath(__file__).replace(os.path.basename(__file__), "") + ".alix"
FLAG_ARG_DICT = { "-d":1, "-r":1, "-l":0, "-ld":0 }

def alix_list():
	commands = {}
	with open(ALIXES, "r") as file:
		cur_command = None
		for line in file:
			if (line[0] != "\t"):
				cur_command = line.replace("\n", "")
				commands[cur_command] = []
			else:
				commands[cur_command].append(line.replace("\t", "").replace("\n", ""))

	if not commands:
		return None
	else:
		return commands

def alix_list_commands():
	command_names = []
	with open(ALIXES, "r") as file:
		for line in file:
			if (line[0] != "\t"):
				command_names.append(line.replace("\n", ""))

	if not command_names:
		return None
	else:
		return command_names

def alix_has_command(command_name):
	command_list = alix_list_commands()
	if command_list:
		return command_name in command_list
	else:
		return False

def alix_delete(command_name):
	assert alix_has_command(command_name), "Alix has no command '%s'" % command_name

	commands = alix_list()
	open(ALIXES, "w").close()

	for command in commands:
		if (command != command_name):
			alix_create(command, commands[command])
		else:
			cmd("rm %s" % command)

def alix_create(command_name, commands, force = False):
	if force:
		try:
			alix_delete(command_name)
		except AssertionError:
			pass

	assert not alix_has_command(command_name), "Alix already has command '%s'" % command_name

	with open(ALIXES, "a") as file:
		file.write("%s\n" % command_name)
		for command in commands:
			file.write("\t%s\n" % command)

	alix_update()

def alix_record(command_name):
	commands_rec = []

	command = None
	while (command != "alix -s"):
		command = str(input("(AlixRec) " + os.getcwd() + ">"))

		cmd(command)
		command_rec.append(command)

	alix_create(command_name, commands_rec)

def alix_update():
	with open(ALIXES, "r") as file:
		cur_command = None
		for line in file:
			if (line[0] != "\t"):
				cur_command = line.replace("\n", "")
				with open("%s.bat" % cur_command, "w") as command_file:
					command_file.write("@ECHO OFF\n")
			else:
				with open("%s.bat" % cur_command, "a") as command_file:
					command_file.write(line.replace("\t", ""))


def main(args):
	assert len(args) != 0, "No args passed to alix command"
	if len(args) == 0:
		print("ERROR: No")
		return None
	else:
		flags = []
		command_name = None
		command = None
		# print("args were: " + str(args))

		i = 0
		while (i < len(args) and args[i][0] == "-"):
			flags.append(args[i])
			i = i + 1

		#No flags
		if (i == 0):
			assert len(args) == 2, "Alix missing number of required args (Given: %s" % str(args) + ")"
			alix_create(args[0], [args[1]])
		#Single flag
		elif (i == 1):
			flag = flags[0]
			command_args = args[1:]
			assert len(command_args) == FLAG_ARG_DICT[flags[0]], "Alix passed wrong number of args for '%s' flag (given %d args)" % (flags[0], len(command_args))

			DELETE_FLAGS = ["--delete", "-d"]
			RECORD_FLAGS = ["--record", "-r"]
			LIST_FLAGS = ["--list", "-l"]
			LIST_DETAILS_FLAGS = ["--listdets", "-ld"]
			FORCE_FLAGS = ["--force", "-f"]

			if flag in DELETE_FLAGS:
				alix_delete(command_args[0])
			elif flag in RECORD_FLAGS:
				alix_record(command_args[0])
			elif flag in LIST_FLAGS:
				print(str(alix_list_commands()))
			elif flag in LIST_DETAILS_FLAGS:
				print(str(alix_list()))
			elif flag in FORCE_FLAGS:
				alix_create(command_args[0], command_args[1], True)


if __name__ == "__main__":
	main(sys.argv[1:])