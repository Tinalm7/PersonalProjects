from Parser import Parser
from Program import Program
from Memory import Memory

import sys

def main():
  # Initialize the parser object (contains the scanner and some helper functions)
  parser = Parser(sys.argv[1])
  memory = Memory(sys.argv[2])
  p = Program()
  p.parse(parser)
  p.semantic(parser)
  p.execute(memory)


if __name__ == "__main__":
    main()