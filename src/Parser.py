import csv
import os

class Parser:
	"""
	Utility object to parse the input
	"""
	def __init__(self, dataFolder="data", inputCSVFile="input.csv"):
		self.filePath = os.path.join(dataFolder, inputCSVFile)
		self.filePath = os.path.abspath(self.filePath)
		self.words = []
		fileExtension = os.path.splitext(self.filePath)[1].lower()
		if fileExtension != ".csv":
			raise RuntimeError("Expected a CSV file. Received %s" % fileExtension)
		if not os.path.isfile(self.filePath):
			raise FileNotFoundError("%s does not exist" % self.filePath)
		print("Parsing %s" % self.filePath)
		with open(self.filePath) as csvFile:
			csvReader = csv.reader(csvFile)
			for line in csvReader:
				if len(line) > 1:
					raise RuntimeError("Each line in the CSV file must be a single word. Received %s" % repr(line))
				self.words.append(line[0])
