from score.score import score_word
from sys import argv as argv 

""" This program generates the possibe list of combinations of words from the given dictionary 

 with the weightage for the given word. With two wildcard character , this runs approximately for 20 seconds.

"""

# Checking for the argument.

try:
    strWord  = argv[1].upper()
    
except IndexError:
    print('Please pass valid argument.')
    quit()

argCount = len(argv)

try:

    if argCount > 2:
        charLetter = argv[2]
        intPosition = int(argv[3])
except IndexError:
    print('Please enter the character and the index position in the format for example , python scrabble.py WORD D 2')
    quit()
except ValueError:
    print('Please enter the correct values for the character and the index position')
    quit()





# Check for maximum number of wild card character in the given word.

try:
    
    if strWord.count('*') + strWord.count('?') > 2:
        raise ValueError("Number of wild cards cannot exceed 2. ") 
except ValueError as e:
    print(e)
    quit()

# Pre process the dictionary.
# Load the dictionary data.

with open("sowpods.txt","r") as infile:
    raw_input = infile.readlines()
    data = [datum.strip('\n') for datum in raw_input]



# Function to check the valid words in the dictionary    

def scrabbleme(strWord, dictword):
    
    """ scrabbleme: Function to generate the list words from the dictionary. """

    
    for chr in dictword:
        if chr not in strWord or dictword.count(chr) > strWord.count(chr): return False
    return True


arrayWords = [strWord]
cleanList=[]

# Generate the wildcard word lists.

def replacewildcards(arrayWords):
    """ This function generates all possible words for the given wildcards characters. """
    global cleanList
    strwildWord=''
    
    if sum([1 for i in arrayWords for j in i if j=='*' or j=='?'])==0:
        #cleanList = cleanList + arrayWords
        return

    for item in arrayWords:
        strwildWord = item
        for i in range(len(item)):
            if item[i]=='*' or item[i]=='?':
                arrayWords =   [item[0:i] + letter + item[i+1:] for letter in ['A','B','C','D','E', 'F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']]
                if sum([1 for i in arrayWords for j in i if j=='*' or j=='?'])==0:
                    cleanList = cleanList + arrayWords

    replacewildcards(arrayWords)

if sum([1 for i in arrayWords for j in i if j=='*' or j=='?'])==0:
    cleanList = arrayWords
else:
    replacewildcards(arrayWords)



# Call the function to preprocess to only the list that contains all the characters that are in the given word
intLength = len(strWord)
result = []

for word in cleanList:
    result = result + [item for item in data if len(item) <= intLength and scrabbleme(word, item) == True and item not in result ]

if argCount > 2:
    result = [item for item in result if len(item)>=intPosition+1]
   
    result = [item for item in result if item[intPosition]==charLetter]

# Final Printing in the sorted order.

print(sorted([( item,score_word(item.lower())) for item in result],key = lambda x: x[1],reverse=True))




