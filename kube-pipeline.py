"""This is main module of the program"""

import sys

from utility import commands


def help():
  """Print helps"""

  print("./kube-pipeline [COMMAND] [OPTIONS]")
  print("COMMAND: ")
  for command in commands.keys():
    print("- {}".format(command))


if __name__ == '__main__':
  """This is the entry of the program"""

  if len(sys.argv) < 2:
    help()
    sys.exit(2)

  try:
    commandClass = commands[sys.argv[1]]
    commandClass().execute()
    sys.exit(0)
  except KeyError:
    print("Invalid command.\n")
    help()
    sys.exit(2)
  except Exception:
    print("Something went wrong. Please try again.")
    sys.exit(2)    