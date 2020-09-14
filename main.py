from src.Parser import Parser
from src.Groupizer import Groupizer

"""
For command line debugging
"""

if __name__ == '__main__':
	parser = Parser()
	groupizer = Groupizer(load=False, parser=parser)
	err = groupizer.save()
	if err: print("Error during save.")
	err = groupizer.load()
	if err: print("Error during load.")
	groupizer = Groupizer(load=True)
	print("Ran with no errors")
