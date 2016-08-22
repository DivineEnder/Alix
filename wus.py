import os
from subprocess import call as cmd


command = ""
while(command != "exit wus"):

	print(os.getcwd() + ">", end="")
	command = str(input())

	print("You entered the command: " + command)

	cmd(command)