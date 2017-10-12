# @Author: DivineEnder
# @Date:   2016-11-29 21:02:44
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-10-12 19:07:05


import sys
import os
from subprocess import call as cmd

import pickle
import argparse
from dotenv import load_dotenv, find_dotenv

class Alix(object):

	def __init__(self):
		# Load environment file variables as local os env variables
		load_dotenv(find_dotenv())
		# Make the local cmds folder if none already there
		if not os.path.exists(os.environ.get("CMDS_PATH")):
			os.makedirs(os.environ.get("CMDS_PATH"))

		# Load some env variables into class
		self.alixes_path = os.environ.get("ALIXES_PATH")
		self.cmds_path = os.environ.get("CMDS_PATH")
		self.alix_path = os.environ.get("ALIX_PATH")

		self.alix_commands = ["list", "show", "create", "edit", "delete", "record"]

		# Preload the stored commands into a dictionary
		self.alixes = self.load_alixes()

	# Parse given args
	def parse(self, args):
		# Setup parser object
		parser = argparse.ArgumentParser(prog = "Alix", description = "Alix provides simple alias command functionality for Windows.")
		parser.add_argument("command", choices = self.alix_commands, help = "Subcommand to run")

		# Parse the first argument passed
		res = parser.parse_args(args[0:1])

		# Call the command's corresponding parser function to parse its args
		getattr(self, res.command + "_parse")(args[1:])

	# Load dictionary of alixes from the specified pickle file
	def load_alixes(self, cmds_file = None):
		cmds_file = self.alixes_path if cmds_file is None else cmds_file
		return pickle.load(open(cmds_file, "rb"))

	# Store the dictionary of alixes in the specified pickle file
	def store_alixes(self, cmds_file = None, alixes = None):
		cmds_file = self.alixes_path if cmds_file is None else cmds_file
		alixes = self.alixes if alixes is None else alixes
		try:
			pickle.dump(alixes, open(cmds_file, "wb"))
			return True
		except Exception as e:
			print("Something went wrong while trying to save the commands to file.")
			print(e)
			return False

	# Clean the given directory of batch files not in the alix dictionary
	def clean(self, dir):
		self.alix_names = list(self.alixes.keys())
		for file in os.listdir(dir):
			if file.endswith(".bat"):
				if not file[0:-4] in self.alix_names and not file == "alix.bat":
					cmd("rm %s%s" % (dir, file))

	# Check whether the given alix name is in use
	def is_alix(self, alix):
		return alix in list(self.alixes.keys())

	# Performing closing updates and checks
	def close(self):
		self.clean(self.alix_path)
		self.clean(self.cmds_path)
		self.store_alixes()

	# Parse arguments for the list command
	def list_parse(self, flags):
		# Create list parser
		list_parser = argparse.ArgumentParser(prog = "alix list", description = "List avaliable alix commands")
		list_parser.add_argument("-v", "--verbose", action = "store_true", help = "Verbose printing of commands")

		# Parse list arguments
		list_flags = list_parser.parse_args(flags)
		# Print alix commands
		for alix in self.alixes.keys():
			self.show(alix, list_flags.verbose)

	# Parse arguments for the show command
	def show_parse(self, flags):
		# Create show parser
		show_parser = argparse.ArgumentParser(prog = "alix show", description = "Examine a single alix")
		show_parser.add_argument("alix", help = "The alias used to call the command")
		show_parser.add_argument("-v", "--verbose", action = "store_true", help = "Verbose printing of the command")

		# Parse show arugments
		show_flags = show_parser.parse_args(flags)

		# Print alix command (error on bad print)
		if not self.show(show_flags.alix, show_flags.verbose):
			show_parser.error("Try the 'list' subcommand to list all alix commands")

	# Display the given alix command
	def show(self, alix, VERBOSE = False):
		if self.is_alix(alix):
			# Print alix and description
			print(" {:15}".format(alix) + str(self.alixes[alix]["desc"]))

			# Print command if verbose
			if VERBOSE:
				for line in self.alixes[alix]["cmd"]:
					print("  | %s" % line)

			# Return show suceeded
			return True
		else:
			print("Could not print alix '%s' (does not exist)" % alix)
			# Return show failed
			return False

	# Parse arguments for the record command
	def record_parse(self, flags):
		# Create the argument parser for the record option of alix
		record_parser = argparse.ArgumentParser(prog = "alix record", description = "Record an alix command")
		record_parser.add_argument("alias", help = "The alias to use for the recorded command")
		record_parser.add_argument("-f", "--force", action = "store_true", help = "Replace any existing alix commands with the new alix command")
		record_parser.add_argument("description", nargs = "?", default = None, help = "Provide a description for the alix")

		# Parse record arguments
		record_flags = record_parser.parse_args(flags)

		# Create the given alix command (records the command within the create function)
		if not self.create(alix = record_flags.alias,
							command = None,
							desc = record_flags.description,
							force = record_flags.force):
			record_parser.error("Either delete the previous alix or use the -f flag when creating")

	# Parse arguments for the create command
	def create_parse(self, flags):
		# Create the argument parser for the create option of alix
		create_parser = argparse.ArgumentParser(prog = "alix create", description = "Create a new alix command")
		create_parser.add_argument("alias", help = "The alix name to use when the command is called")
		create_parser.add_argument("-f", "--force", action = "store_true", help = "Replace any existing alix commands with the new alix command")
		create_parser.add_argument("command", help = "The actual batch command that should execute. Separate command lines by a \\n")
		create_parser.add_argument("description", nargs = "?", default = None, help = "Provide a description for the alix")

		# Parse the create arguments
		create_flags = create_parser.parse_args(flags)

		# Create the alix command
		if not self.create(alix = create_flags.alias,
							command = create_flags.command,
							desc = create_flags.description,
							force = create_flags.force):
			create_parser.error("Either delete the previous alix or use the -f flag when creating")

	# Create a given alix command
	def create(self, alix, command, desc, force):
		# Make sure force is turned on if the alix has already been created
		if self.is_alix(alix) and not force:
			print("Alix '%s' is already in use." % alix)
			# Return create failed
			return False
		# Create the alix
		else:
			# Description carries to next command if overwritting previous comand without a description
			if self.is_alix(alix) and desc is None:
				desc = self.alixes[alix]["desc"]

			# Setup alixes dictionary entry (replaces old entry if there is one)
			self.alixes[alix] = { "cmd": [], "desc": desc }

			# Create the upper level batch file that calls the actual file to execute the commands
			with open("%s%s.bat" % (self.alix_path, alix), "w") as command_file:
				command_file.write("@ECHO OFF\n")
				command_file.write("%s%s.bat\n" % (self.cmds_path, alix))

			# Create the lower level batch file that actually executes the command
			with open("%s%s.bat" % (self.cmds_path, alix), "w") as command_file:
				command_file.write("@ECHO OFF\n")
				# Already have a command, split it up and add it to the dictionary and batch file
				if not command is None:
					for command_line in command.split("\\n"):
						command_file.write(command_line + "\n")
						self.alixes[alix]["cmd"].append(command_line)

				# Otherwise need to record command
				# TODO:: Update recoding code/functionality
				else:
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
							return False
						elif command == "alix -d":
							if len(commands_rec) > 0:
								print("Deleted previous command '%s'.\n" % commands_rec[-1])
								commands_rec = commands_rec[:-1]
							else:
								print("You have not yet recorded any commands.\n")

					# Write recorded commands to file and update dictionary
					for command_line in commands_rec:
						command_file.write(command_line + "\n")
						self.alixes[alix]["cmd"].append(command_line)

			print("Created alix command '%s'" % alix)

			# Return created suceeded
			return True

	# Parse arguments for edit command
	def edit_parse(self, flags):
		# Create the argument parser for the edit option of alix
		edit_parser = argparse.ArgumentParser(prog = "alix edit", description = "Edit an alix command")
		edit_parser.add_argument("alias", help = "The alias of the command to edit")
		edit_parser.add_argument("-n", "--name", help = "Edit the alias for a command")
		edit_parser.add_argument("-d", "--desc", help = "Edit the description for a command")

		# Parse edit arguments
		edit_flags = edit_parser.parse_args(flags)

		if not self.edit(alix = edit_flags.alias,
							name = edit_flags.name,
							desc = edit_flags.desc):
			edit_parser.error("Use the 'list' subcommand to list all alixes")

	# Edit an alix command without changing the underlying command
	def edit(self, alix, name, desc):
		if not self.is_alix(alix):
			print("No alix '%s' to edit" % alix)
			# Return edit failed
			return False
		else:
			# If both arugments are missing the user did not pass them in and so wants to edit the actual script
			if name is None and desc is None:
				# Get the editor that should be used (default to vim)
				editor = os.environ.get("EDITOR") if os.environ.get("EDITOR") else "vim"
				# Open the editor with the given alix file
				cmd([editor, "%s%s.bat" % (self.cmds_path, alix)])
				# Finished editing alix
				return True

			# Change alix description (must be first in order to avoid name change confusion)
			if not desc is None:
				self.alixes[alix]["desc"] = desc

			# Change alix name
			if not name is None:
				# Move upper level batch file to new name
				cmd("mv %s%s.bat %s%s.bat" % (self.alix_path, alix, self.alix_path, name))
				# Change the upper level file to call the new lower file
				with open("%s%s.bat" % (self.alix_path, name), "w") as file:
					file.write("@ECHO OFF\n")
					file.write("%s%s.bat\n" % (self.cmds_path, name))
				# Move lower level batch file to new name
				cmd("mv %s%s.bat %s%s.bat" % (self.cmds_path, alix, self.cmds_path, name))
				# Change alix name to new name in dictionary
				self.alixes[name] = self.alixes.pop(alix)

			# Return edit suceeded
			return True

	# Parse arguments for delete command
	def delete_parse(self, flags):
		# Create the argument parser for the delete option of alix
		delete_parser = argparse.ArgumentParser(prog = "alix delete", description = "Delete an alix command")
		delete_parser.add_argument("alias", help = "The alix command to delete")

		# Parse delete arguments
		delete_flags = delete_parser.parse_args(flags)

		# Delete given command
		if not self.delete(delete_flags.alias, delete_parser):
			delete_parser.error("Check a list of commands using the 'list' subcommand")

	# Delete the given alix command from the dictionary (does not remove batch files, that is done on close)
	def delete(self, alix, parser):
		if self.is_alix(alix):
			# Remove command from dictionary of commands
			del self.alixes[alix]
			# Return delete suceeded
			return True
		else:
			print("No alix '%s' to delete" % alix)
			# Return delete failed
			return False

def main(args):
	alix = Alix()
	alix.parse(args)
	alix.close()

if __name__ == "__main__":
	main(sys.argv[1:])
