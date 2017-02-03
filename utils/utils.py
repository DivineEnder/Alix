import os

def alix_path():
	return "\\".join(os.path.realpath(__file__).replace(os.path.basename(__file__), "")[:-1].split("\\")[:-1]) + "\\"

def alixes_path():
	return alix_path() + ".alix"

def env_path():
	return alix_path() + ".env"

def cmds_path():
	return alix_path() + "cmds\\"

def docs_path():
	return alix_path() + "Docs"

def flags_path():
	return docs_path() + "\\flags"

def load_env():
	ENV = {}
	with open(env_path(), "r") as environment:
		for line in environment:
			line = line.replace("\n", "")
			var_name, var = line.split("=")
			ENV[var_name] = var

	if not os.path.exists(ENV["CMDS_PATH"]):
		os.makedirs(ENV["CMDS_PATH"])
		
	return ENV