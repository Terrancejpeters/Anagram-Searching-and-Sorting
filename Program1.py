'''
Terrance Peters
CS 311 Program Assignment 1
Due Monday, October 23rd 2017.

A Program for sorting and identifying anagrams within a given dictionary.
Please view comments below regarding individual run time. In my tests I found the following run times:

All calculations were found on the Linux EdLab servers

Dict1
0.6769 seconds
Total number of anagrams: 67606

Dict2
47.23 seconds
Total number of anagrams: 320750


'''

import sys
import time

#a count of all the words.
wordCount = 0

#The Modulus. This is made global as it is present throughout the program and we don't
#want to worry about multiple calculations.
modu = 0
'''
A note about the prime numbers:

I just listed the first 26 prime members, however it's been pointed out
that in practical applications, it may be better to research a list
of the most common letters in the english language and give smaller values
to the more prevalent letters so as to minimize the calculations. Again though
this is only in the semantics of the english language, as if we were given a truly 
random dictionary each letter would be as likely and thus the prime number associated
with a letter would be irrelevant.
'''
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
def main(argv):
	#Timer, to check runtime
	timeStart = time.time()
	#Check if the dictionary input is present and functional.
	try:
		DictInput = open(argv[0],'r')
	#if we are unable to, tell the user there is a problem and exit the system
	except IOError: 
		print "Dictionary not input correctly. The program will exit"
		sys.exit()
	#The Anagram Class we use for storing all values. We use the Hash Table specified below
	anagramClass = HashTable()
	
	#Count the number of words in the dictionary. Runs in O(n) time.
	for word in DictInput:
		global wordCount
		wordCount += 1

	#Calculate the modulus, assuming we cannot use libraries as this is apart of the hash sort later
	for num in range(1,28):
		global modu
		modu = 2 ** num
		if modu > wordCount and (float(wordCount) / modu) < (2.0/3.0):
			break
	#Return to the beginning of Dictionary Input
	DictInput.seek(0)
	#For every word in the input...
	#1) remove white space or carriage returns
	#2) add it to the anagram class
	for word in DictInput:
		aWord = WordSorter(word.strip())
		anagramClass.insert(aWord)
	#Close the dictionary, we good here
	DictInput.close()

	'''
	try to open or create an output file. This shouldn't yield any issues
	unless the user is running it in a place they do not have write priviledges to
	'''
	try:
		AnaOut = open(argv[1], 'w')
		for anagram in anagramClass.table:
			if anagram:
				AnaOut.write(" ".join(anagram[1]))
				AnaOut.write("\n")
		AnaOut.close()
	except IOError:
		print "Output environment improperly provided. System will exit"
		sys.exit()
	
	#print relevant run information
	print "Anagram classes total:", anagramClass.size
	print "Runtime", (time.time() - timeStart)




#Our hash table, how we hold all dictionary values
class HashTable:
	#Initalize. Pretty simple operation in O(1) time
	def __init__(self):
		self.table = []
		self.size = 0
	#The Insertion function. adds words to our table 
	def insert(self, addWord):
		if len(self.table) <= addWord.hash:
			#Pretty much a collection of O(1) time operations
			#Check the table size, if too small make room for more elements
			#Keep track of the difference between the table len and the Hash position for this word
			diff = (addWord.hash - len(self.table)) + 1
			#multiply to fill 
			self.table[len(self.table):] = [None] * diff
			#Place the word based on it's long hash
			self.table[addWord.hash] = (addWord.longHash, [addWord.word])
			#increase the hash Table size
			self.size += 1
		elif self.table[addWord.hash]:
			#Check and Append if necessary. More O(1) time operations
			if self.table[addWord.hash][0] == addWord.longHash:
				self.table[addWord.hash][1].append(addWord.word)
			else: 
				#This occurs if there is a conflict, resolve via chaining
				addWord.hash += 1
				while(True):
					#Looping O(1) Operations. Should be at most O(n) time once the loop is complete
					if addWord.hash == len(self.table):
						self.table.append((addWord.longHash,[addWord.word]))
						self.size += 1
						break
					elif self.table[addWord.hash] is None:
						self.table[addWord.hash] = (addWord.longHash, [addWord.word])
						self.size += 1
						break
					elif self.table[addWord.hash][0] == addWord.longHash:
						self.table[addWord.hash][1].append(addWord.word)
						break
					else:
						addWord.hash+= 1
		else:
			#Final O(1) time operations. If all other conditionals aren't met, just add the word and increase the size
			#Hooray for no conflicts.
			self.table[addWord.hash] = (addWord.longHash, [addWord.word])
			self.size += 1


#Class that handles word sorting, specifcially alphabetical sorting
class WordSorter:
	#Initalizer. O(1) time
	def __init__(self, word):
		self.word = word
		self.longHash, self.hash = self.sortAlpha()
	#Alphabetical sorter. This is a slight variation of normal counting sort since we need to account for alphabetical order.
	#We resolve conflicts via open addressing since we create open space within the table to fit all words
	#within the dictionary. Finally we relay the strings sorted using the regular counting sort
	#Total time: O(k + d) first sort + O(k) second sort
	def sortAlpha(self):
		C = []
		for i in range(26):
		#Append space for every letter. O(1) time (... or O(26) if we're being specific)
			C.append(0)
		#Letter translation from Ascii codes. Chars subtract 97 since the letter A begins at 97, B 98, and so on. 
		#makes keeping our tables more orderly and easier to operate on later, only takes O(d) time
		for j in range(len(self.word)):
			C[ord(self.word[j]) - 97] += 1
		hash = 1
		for i in range(26):
			hash *= primes[i] ** C[i]
		return hash, (hash % modu)

	#We just remove the whitespace around words and carriage returns/new line indicators that may be
	#in the original dictionary file.
	def __repr__(self):
		return self.word.strip()

#Check that the proper arguemtns are given before running our main method.
#If they're incorrect, throw an error and tell the user to fix it.
if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1:])
    else:
        print "Please provide to arguments (Should be in the form Python Program1.py Argument1 Argument2). The first argument should be a dictionary, second should be a file to write outputs"
