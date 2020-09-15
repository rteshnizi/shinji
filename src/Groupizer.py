import json
import os
from typing import List, Dict
from src.Parser import Parser
from src.Utils.FlaskErrors import GenericError, NotInitialized

class Groupizer:
	def __init__(self, load, parser: Parser=None, delimiter="_", dataFolder="data", fileName="Groupizer.json"):
		self._dataFolder = dataFolder
		self._fileName = fileName
		# Will be set to true upon adding/moving a word or group
		self._dirty = False
		# The path to the JSON file to maintain changes. Will be set once save/load method is called
		self.jsonPath = None
		# Dictionary of group names to words
		self.groups: Dict[str, List[str]] = {}
		# Reverse of the above dict
		self._wordToGroupMap: Dict[str, str] = {}
		# Delimiter used in the words to specify categories in one word. e.g., A_B_C and A_B_D yield a group A_B.
		self.delimiter = delimiter
		# List of all words to be processed
		self.allWords: List[str]
		if load:
			print("Loading from file...")
			err = self.load()
			if err: raise GenericError(err)
			self.allWords = list(self._wordToGroupMap.keys())
		else:
			print("Grouping %d words..." % len(parser.words))
			self.allWords = parser.words
			self._build()

	def __repr__(self):
		return "Groupizer: %d words" % len(self.allWords)

	def _buildMinGroups(self, words: List[str]) -> Dict[str, List[str]]:
		"""
		Deprecation Note
		===
		I had to abandon this method after the question was calrified to me.
		"""
		words.sort()
		i = 0
		while i < len(words):
			word = words[i]
			parts = word.split(self.delimiter)
			print("Creating group for '%s'" % word)
			if i == len(words) - 1:
				print("Adding '%s' to group '%s'" % (nextWord, prefix))
				self.groups[word] = [word]
			prefixCandidate = None
			prefix = None
			startInd = i
			while i < len(words) - 1:
				nextWord = words[i + 1]
				if i == startInd:
					for numWords in range(1, len(parts) + 1):
						prefixCandidate = self.delimiter.join(parts[:numWords])
						if nextWord.startswith(prefixCandidate): continue
						prefix = self.delimiter.join(parts[:numWords - 1])
						break
					if not prefix: prefix = word
					print("Selected group: '%s'" % prefix)
					self.groups[prefix] = [word]
					i += 1
				if not nextWord.startswith(prefix): break
				print("Adding '%s' to group '%s'" % (nextWord, prefix))
				self.groups[prefix].append(nextWord)
				i += 1

	def _groupName(self, index1, index2) -> str:
		"""
		Given two indices of the words in the array,
		this method finds the longest common prefix between the two.
		**Note**: This method assumes that the array of words is sorted.
		"""
		maxIndex = len(self.allWords) - 1
		if index1 > maxIndex and index2 > maxIndex: return None
		if index1 > maxIndex: return self.allWords[index2]
		if index2 > maxIndex: return self.allWords[index1]
		if index1 < 0 and index2 < 0: return None
		if index1 < 0: return self.allWords[index2]
		if index2 < 0: return self.allWords[index1]
		smallerIndex = min(index1, index2)
		largerIndex = max(index1, index2)
		word1 = self.allWords[smallerIndex]
		word2 = self.allWords[largerIndex]
		parts = word1.split(self.delimiter)
		prefixCandidate = None
		prefix = None
		broke = False
		for numWords in range(1, len(parts) + 1):
			prefixCandidate = self.delimiter.join(parts[:numWords])
			if word2.startswith(prefixCandidate): continue
			prefix = self.delimiter.join(parts[:numWords - 1])
			broke = True
			break
		prefix = prefix if broke else word1
		return prefix

	def _build(self) -> Dict[str, List[str]]:
		"""
		Given the list of words, populate the dictionary of the group names to the words in the group.
		The time complexity is O(n log n) because of the sort operation.

		To populate the groups, we iterate the sorted array, comparing it to the previous and next words.
		Whichever yields a longer prefix is then used as the group for this word.
		This logic holds because the array is sorted.

		Notice that, if a word does not belong to a group, a group is made whose name is the same as the word.
		This is intentional, as keeping the data uniform, will make consuming of the data more predictable.
		"""
		self.allWords.sort()
		i = 0
		while i < len(self.allWords):
			word = self.allWords[i]
			print("Finding group for '%s'" % word)
			group1 = self._groupName(i - 1, i)
			group2 = self._groupName(i, i + 1)
			if group1 is None and group2 is None: raise RuntimeError("WTF?")
			if not group1:
				selectedGroup = group2
			elif not group2:
				selectedGroup = group1
			else:
				selectedGroup = group1 if len(group1) > len(group2) else group2
			if not selectedGroup:
				selectedGroup = word
			self.addToGroup(selectedGroup, word)
			i += 1

	def addToGroup(self, groupName, word) -> str:
		"""
		Returns
		===
		Error string if an exception occurred, empty string otherwise.
		"""
		try:
			if groupName not in self.groups.keys():
				self.createGroup(groupName)
			isNewWord = word not in self._wordToGroupMap.keys()
			if isNewWord:
				print("Adding '%s' to group '%s'" % (word, groupName))
			else:
				oldGroup = self._wordToGroupMap[word]
				print("Moving '%s' from group '%s to '%s'" % (word, oldGroup, groupName))
				self.groups[oldGroup].remove(word)
			self.groups[groupName].append(word)
			self._wordToGroupMap[word] = groupName
			self._dirty = True
			return ""
		except Exception as err:
			return repr(err)

	def createGroup(self, groupName) -> str:
		"""
		Returns
		===
		Error string if an exception occurred, empty string otherwise.
		"""
		try:
			if groupName in self.groups.keys():
				msg = "Group '%s' already exists." % groupName
				print(msg)
				return msg
			self.groups[groupName] = []
			print("Created group: '%s'" % groupName)
			self._dirty = True
			return ""
		except Exception as err:
			return repr(err)

	def deleteGroup(self, groupName) -> str:
		"""
		Returns
		===
		Error string if an exception occurred, empty string otherwise.
		"""
		try:
			if groupName not in self.groups.keys():
				msg = "Group '%s' does not exist." % groupName
				print(msg)
				return msg
			if len(self.groups[groupName]) > 0:
				msg = "Group '%s' is not empty." % groupName
				print(msg)
				return msg
			del self.groups[groupName]
			print("Deleted group: '%s'" % groupName)
			self._dirty = True
			return ""
		except Exception as err:
			return repr(err)

	def save(self) -> str:
		"""
		Save the in-memory data to a JSON file.
		If later it is decided that the data should be stored in a different database, the implementation can be adapted.

		Returns
		===
		Error string if an exception occurred, empty string otherwise.
		"""
		try:
			if not self._dirty: return ""
			self.jsonPath = os.path.join(self._dataFolder, self._fileName)
			self.jsonPath = os.path.abspath(self.jsonPath)
			data = {
				"groups": self.groups,
				"_wordToGroupMap": self._wordToGroupMap
			}
			with open(self.jsonPath, 'w') as jsonFile:
				json.dump(data, jsonFile)
			self._dirty = False
			return ""
		except Exception as err:
			return repr(err)

	def load(self) -> str:
		"""
		If a JSON file is available that holds the stored data (persistent data), it is loaded into memory.

		Returns
		===
		Error string if an exception occurred, empty string otherwise.
		"""
		try:
			self.jsonPath = os.path.join(self._dataFolder, self._fileName)
			self.jsonPath = os.path.abspath(self.jsonPath)
			if not os.path.isfile(self.jsonPath):
				print("%s does not exist to load from." % self.jsonPath)
				raise NotInitialized()
			with open(self.jsonPath, 'r') as jsonFile:
				data = json.load(jsonFile)
			self.groups = data["groups"]
			self._wordToGroupMap = data["_wordToGroupMap"]
			return ""
		except NotInitialized as err:
			raise err
		except Exception as err:
			return repr(err)
