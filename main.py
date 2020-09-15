from src.Parser import Parser
from src.GroupService import GroupService

"""
For command line debugging
"""

if __name__ == '__main__':
	parser = Parser()
	GroupService = GroupService(load=False, parser=parser)
	err = GroupService.save()
	if err: print("Error during save.")
	err = GroupService.load()
	if err: print("Error during load.")
	GroupService = GroupService(load=True)
	print("Ran with no errors")
