import sys
import os
from subprocess import call as cmd
from pprint import pprint
import json

from utils.utils import alix_path, docs_path, flags_path
from utils.utils import load_env

try:
	ENV = load_env()
except FileNotFoundError:
	raise EnvironmentError("No Environment file found for Alix. Alix needs several system variables defined for it. Run setup.py to properly install Alix.")

def read_flags():
	flag_dict = {}
	with open("%s\\flags.list" % docs_path(), "r") as flag_list:
		for line in flag_list:
			line = line.replace("\n", "")
			flags, args = tuple([item.split(",") for item in filter(None, line.split(":"))])
			args = list(map(int, args))
			for flag in flags:
				flag_dict[flag] = { "args": args }
	return flag_dict

def alix_list():
	commands = {}
	with open(ENV["ALIXES_PATH"], "r") as file:
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
	with open(ENV["ALIXES_PATH"], "r") as file:
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
	if not alix_has_command(command_name):
		print("Alix has no command '%s'." % command_name)
		print("You can use '-l' to print all alix commands.\n")
		return

	commands = alix_list()
	open(ENV["ALIXES_PATH"], "w").close()

	for command in commands:
		if (command != command_name):
			alix_create(command, commands[command], silent = True)
		else:
			cmd("rm %s%s.bat" % (ENV["ALIX_PATH"], command))
			cmd("rm %s%s.bat" % (ENV["CMDS_PATH"], command))

	print("Deleted alix named '%s'." % command_name)

def alix_create(command_name, commands, force = False, silent = False):
	if alix_has_command(command_name):
		print("Alix already has command '%s'" % command_name)
		if input("Would you like to replace it (y/n) : ").lower() == "y":
			force = True
		else:
			print("Did not create command '%s'." % command_name)
			return

	if force:
		try:
			alix_delete(command_name)
		except AssertionError:
			pass

	with open(ENV["ALIXES_PATH"], "a") as file:
		file.write("%s\n" % command_name)
		for command in commands:
			file.write("\t%s\n" % command)

	alix_update()

	if not silent:
		print("Created alix command '%s'.\n" % command_name)

def alix_record(command_name = None):
	commands_rec = []

	command = None
	print("Alix is now recording commands.\nUse 'alix -qw' to save what has been recorded as a command.\nUse 'help' for more information.\n")
	while (command != "alix -qw"):
		command = str(input("(AlixRec) " + os.getcwd() + ">"))

		if not (command == "alix -d" or command == "alix -q" or command == "alix -qw" or command.lower() == "help"):
			cmd(command, shell = True)
			commands_rec.append(command)
		elif command.lower() == "help":
			print("Alix record sits behind the shell, noticing and recording your commands.")
			print("Since Alix is a python script any commmand typed will be fed through python to the command line.")
			print("Alix was created by DivineEnder.")
			print("To stop recording use the command: 'alix -qw'")
			print("To quit without saving a command use the command: 'alix -q'")
			print("To delete a previously recorded command use: 'alix -d'\n")
		elif command == "alix -q":
			print("No command was saved.\n")
			return
		elif command == "alix -d":
			if len(commands_rec) > 0:
				print("Deleted previous command '%s'.\n" % commands_rec[-1])
				commands_rec = commands_rec[:-1]
			else:
				print("You have not yet recorded any commands.\n")

	if command_name == None:
		command_name = input("Print please enter the command name you would like associated with your recorded actions: ")
	
	alix_create(command_name, commands_rec)

def alix_update():
	with open(ENV["ALIXES_PATH"], "r") as file:
		cur_command = None
		for line in file:
			if (line[0] != "\t"):
				cur_command = line.replace("\n", "")
				with open("%s%s.bat" % (ENV["ALIX_PATH"], cur_command), "w") as command_file:
					command_file.write("@ECHO OFF\n")
					command_file.write("%s%s.bat\n" % (ENV["CMDS_PATH"], cur_command))
				with open("%s%s.bat" % (ENV["CMDS_PATH"], cur_command), "w") as command_file:
					command_file.write("@ECHO OFF\n")
			else:
				with open("%s%s.bat" % (ENV["CMDS_PATH"], cur_command), "a") as command_file:
					command_file.write(line.replace("\t", ""))

def alix_man(page = "default", is_flag = False):
	if is_flag:
		man_path = "%s\\%s.man" % (flags_path(), page)
	else:
		man_path = "%s\\%s.man" % (docs_path(), page)
	
	with open(man_path, "r") as man:
		for line in man:
			print(line, end = "")
	print("\n")

def main(args):
	flag_dict = read_flags()

	if len(args) == 0:
		alix_man()
	else:
		flags = []
		command_name = None
		command = None

		i = 0
		while (i < len(args) and (args[i][0] == "-" or args[i][0:1] == "--")):
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
			num_flag_args = flag_dict[flag]["args"]
			assert len(command_args) in num_flag_args, "Alix passed wrong number of args for '%s' flag (given %d args)" % (flags[0], len(command_args))

			DELETE_FLAGS = ["--delete", "-d"]
			RECORD_FLAGS = ["--record", "-r"]
			LIST_FLAGS = ["--list", "-l"]
			LIST_DETAILS_FLAGS = ["--list-details", "-ld"]
			FORCE_FLAGS = ["--force", "-f"]
			HELP_FLAGS = ["--help", "-h"]

			if flag in DELETE_FLAGS:
				alix_delete(command_args[0])
			elif flag in RECORD_FLAGS:
				if (len(command_args) > 0):
					alix_record(command_args[0])
				else:
					alix_record()
			elif flag in LIST_FLAGS:
				pprint(alix_list_commands(), indent = 2)
			elif flag in LIST_DETAILS_FLAGS:
				pprint(alix_list(), indent = 2)
			elif flag in FORCE_FLAGS:
				alix_create(command_args[0], command_args[1], True)
			elif flag in HELP_FLAGS:
				alix_man()
				for file in os.listdir(flags_path()):
					if file.endswith(".man"):
						print("%s:" % file.replace(".man", ""))
						alix_man(file.replace(".man", ""), is_flag = True)
				# for root, dirs, files in os.walk(os.path.realpath(__file__).replace(os.path.basename(__file__), "")):
					# for name in files:
					# 	if name.endswith(".man") and not name == "default.man":
					# 		print("%s:" % name.replace(".man", ""))
					# 		alix_man(page = name.replace(".man", ""))
					# 		print()
				print()
				# alix_man()
			else:
				alix_man()
		else:
			alix_man()


if __name__ == "__main__":
	main(sys.argv[1:])