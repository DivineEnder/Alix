# -*- coding: utf-8 -*-
# @Author: David Anuta
# @Date:   2016-12-22 15:12:28
# @Last Modified by:   David Anuta
# @Last Modified time: 2017-01-24 18:10:34

import os
from subprocess import call as cmd
from tkinter import Tk as tk
from tkinter import messagebox as message
from tkinter import filedialog as dialog

from utils.utils import alix_path, env_path, alixes_path, cmds_path

import functools

def trackcalls(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		resp = func(*args, **kwargs)
		wrapper.called = True
		wrapper.resp = resp
		return resp
	wrapper.called = False
	wrapper.resp = None
	return wrapper

def write_env_file(**env_vars):
	with open(".env", "w") as environment:
		for env_var in env_vars:
			environment.write("%s=%s\n" % (env_var, env_vars[env_var]().replace("\\", "/")))

@trackcalls
def py3_dir_path():
	if not py3_dir_path.called:
		tk().withdraw()
		message.showinfo("Python 3 Path", "Please select the directory in which Python 3 is installed on this machine.")
		dir_path = dialog.askdirectory(initialdir = "C:\\", mustexist = True, title = "Python 3 Path Finder")
	else:
		dir_path = py3_dir_path.resp

	return dir_path

def py3_path():
	dir_path = py3_dir_path()
	execs = [file for file in os.listdir(dir_path) if file.endswith(".exe") and file.startswith("python")]
	file_path = dir_path + "\\" + [file for file in execs if not file == "pythonw.exe"][0]
	return file_path

def install():
	write_env_file(
		PY3_PATH = py3_dir_path,
		PY3_EXEC_PATH = py3_path,
		ALIX_PATH = alix_path,
		ALIXES_PATH = alixes_path,
		ENV_PATH = env_path,
		CMDS_PATH = cmds_path)

	cmd("setx ALIX_HOME %s" % alix_path())

	print("Env file created. Alix should be setup.\nHappy alixing!")

def main():
	try:
		open(".env", "r").close()
		print("WARNING: Running setup will reset Alix .env file.\nThis will reset any preferences you have previously set and they will have to be added back in manually.")
		if input("Would you like to continue Alix setup (y/n) : ").lower() == "y":
			install()
		else:
			print("Quitting install...")

	except FileNotFoundError:
		install()

if __name__ == '__main__':
	main()