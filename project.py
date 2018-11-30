'''
Alexander J. Bates
Final Project -- IGPI:5110
December 6, 2018
'''

'''
project stub

State any assumptions you make here. Note these should not contradict
any aspect of the project description.

You may create additional attributes for either class as needed for your assignment.

You may need to use regular expressions. While we will do this in class,
you may want to get a head start and look at:

http://www.tutorialspoint.com/python/python_reg_expressions.htm

'''


import re
import os

# Modules needed later in Poems and Nouns classes.
from string import punctuation as punct
# import nltk # Used for SentiWordNet
from nltk.corpus import sentiwordnet as swn
# from testSentiWordNet import estimate_sentiment
# from contractions import CONTRACTION_MAP

class Poems(object):
    '''
    A class for holding each poem and its attributes
    Assume that there are a large number of poems in the input file.
    
    Attributes of interest:
    poemId: a sequential id for the poem instances, starting at 1
    title: the title of the poem
    author: the name of the person who wrote it
    text: the contents of the poem without any changes
    numberLines: an integer holding the number of non empty lines in the poem
        (not counting the title - author line)
    words: a dictionary with each non trivial word in the poem as key
        and its frequency as value, you may add other information if needed
    nouns: a dictionary with each non trivial noun in the poem as key
        and its frequency as value, you may add other information if needed
        
    non trivial in above means not a stopword and contractions have been expanded.
    I will give you a list of contractions.

    The nltk collection includes a stop word list in a folder called stopwords, use this
    
    sentiment: a rating obtained using sentiwordnet

    I will give you a program to compute sentiment using nltk

    please also add a suitable print method to print out the poem in as
    close to the original format as possible. Input to this method is a poemId
    
    -----Discuss strategy-----

    # Does the self.text attribute count the title - author line? 
    
    '''
    _allPoems = []
    _curPoemId = 1
    def __init__(self,
                 title,
                 author,
                 text
                 ):
        self.poemId = Poems._curPoemId
        Poems._curpoemID += 1
        Poems._allPoems.append(self)
        self.title = title # revisit? 
        self.author = author # revisit?
        self.text = text # Does the self.text attribute count the title - author line?
        self.numberLines = None # revisit.
        self.words = None # revisit.
        self.nouns = None # revisit.
        self.sentiment = None # revisit. 
        pass

    def getfrequency(self, word):
        return self.words[word] ''' Will work, provided self.words is a
                                    dictionary of the form { word:freq }.'''
    
    def __lt__(self, other):
        return self.sentiment < other.sentiment
        # this one is actually complete, provided we get sentiment right. 
    
class Nouns(object):
    '''
    a class for holding non trivial nouns that appear in the poems you process
    For each non trivial noun record the following attributes
    
    noun: the noun itself
    nounId: a sequential id for the noun instances, starting at 1
    synset: the first synset for the noun that you find in wordnet.
    (Note if there is no synset with part of speech (pos) noun for a word
    then do not create an instance for this word)
    definition: the definition for the noun in the synset
    frequency: number of times the noun occurs in the whole set of poems
    pidlist: a list of poemIds in which the noun occurs

    '''

    _allNouns = {}
    _curNounId = 1
    def __init__(self, noun):
        # Note that nouns must be non-trivial. 
        # need self.synset first. 
        self.noun = noun
        if self.noun not in Nouns._allNouns:
            self.nounId = Nouns._curNounId
            Nouns._curNounId +=1
            Nouns._allNouns[self.noun] = self.nounId
        else:
            self.nounId = Nouns._allNouns[self.noun]
        self.synset = None # Revisit. 
        self.definition = None # Revisit.
        self.frequency = None # Revisit.
        self.pidlist = None # Revisit.
        pass

def wordtrain(train):
    if len(train)>=100:
        return train
    else:
        pass # fill in later. Function must be recursive.

def Problem5(mystr):
    i = (len(mystr) >= 7 and len(mystr) < 10)
    ii = any([p in mystr for p in punct])
    iii = mystr.lower() != mystr
    iv = any([mystr in poem.words for poem in Poems._allPoems])
    return all([i, ii, iii, iv])
    # be sure to test this one. 

cwd = os.getcwd()
poemsfile = cwd + '\\Poems_new_2018.txt'
with open(poemsfile, 'r') as myPoems:
    #print myPoems.read()
    pass
