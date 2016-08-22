import sys
from subprocess import call as cmd

def main(args):
	if len(args) == 0:
		print("ERROR: No command(s) passed into alias command")
		return None

if __name__ == "__main__":
	main(sys.argv[1:])