'''
Alexander J. Bates
Final Project -- IGPI:5110
December 6, 2018
'''

'''
Usage:

To do all that was stated in the file ProjectDescription.pdf, all the
grader needs to do is run this file, 'project.py'. To read in a different
poems file, the grader will need to change the line below that says,
'poemsfile = cwd + '\\Poems_new_2018.txt', placing the .txt file containing
the other poems in the same folder as 'project.py'. 
'''

# Module(s) needed to read in the file Poems_new_2018.txt
import os

# Modules needed later in Poems and Nouns classes.
import re
from string import punctuation as punct
import nltk 
from nltk.corpus import stopwords
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import      wordnet as  wn
from testSentiWordNet import estimate_sentiment
''' note that all 'print' statements in testSentiWordNet.py have been
commented out. '''
from contractions import CONTRACTION_MAP

punctnoapos = punct[:6] + punct[7:]
# punctuation without apostrophes

englishstopwords = stopwords.open('english').read()[:-1]
# remove last character since it is '\n'

stopwordslist = englishstopwords.split('\n')
# make english stopwords a list

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
    sentiment: a rating obtained using sentiwordnet
        
    non trivial in above means not a stopword and contractions have been expanded.
    
    -----Discuss strategy-----

    The private variable Poems._allPoems was used to store all initialized
    Poems instances. Poems._curPoemId was used to assign ascending (hence
    unique) PoemId's to each Poems instance. Lastly, Poems._allPoemswords
    was used to store *all* words of all Poems and their frequency across
    all poems.

    To get the sentiment score for each poem, I used the estimate_sentiment
    function much like a black box on the text of the poem using the
    getpoemtext() method.
    '''
    _allPoems = []
    _curPoemId = 1
    _allPoemswords = set() # Note these will be only nontrivial words
    def __init__(self,
                 title,
                 author,
                 text
                 ):
        ''' input: title (str), author (str), and text (str)
            returns: Poems instance with the attributes described above. 
        '''
        self.poemId = Poems._curPoemId
        Poems._curPoemId += 1
        Poems._allPoems.append(self)

        # Define the essential, canonical attributes of the Poems instance:
        self.title = title 
        self.author = author 
        self.text = text

        # Define the contingent attributes of the Poems instance: 
        self.numberLines = self.getnumberLines() 
        self.words = self.getnontrivialwords() # make note about lc and Prob5
        Poems._allPoemswords.update([word for word in self.words])
        self.nouns = self.getnontrivialnouns()
        self.sentiment = estimate_sentiment(self.getpoemtext())[1] 
        pass

    """ # This method unneccessary. 
    def getfrequency(self, word):
        ''' Will work, provided self.words is a dictionary of the form
        { word:freq }. Note that this function does not count stopwords
        or contractions! '''

        # Resolve the issue of whether our dictionary should be case-sensitive
            # It isn't. 
        return self.words[word]
    """

    """
    def getverystrippedpoemtext(self):
        strippedtext = self.getpoemtext()
        verystrippedtext = strippedtext.strip()
        return verystrippedtext
    """

    def getlines(self):
        ''' Method for obtaining the lines of the poem (omitting
        newlines and indentation. 
        
            returns: splitlines (list) of all lines (strings) in the poem with 
        whitespaces removed
        '''
        verystrippedtext = self.getpoemtext().strip()
        splitlines = re.split('[\s^\n]*\n+[\s^\n]*', verystrippedtext)
        return splitlines

    def getnumberLines(self):
        ''' Method for obtaining the number of lines (not counting blank
        lines in Poems instance 'self'.
        
            returns: (int) of lines in the poem (not counting blank lines)
        '''
        splitlines = self.getlines()
        return len(splitlines)

    def getallwords(self):
        ''' Method for obtaining all words in Poems instance 'self'. 

            returns: all words (in a list) in the text of the poem, not
        including title and author line, nor whitespaces. This does however
        include stopwords and contractions. Capitalization from the original
        poem text will be retained.
        '''
        
        """ ### OLD VERSION OF THE PROGRAM ###
        # In this version, All words will retain their
        # capitalization and any punctuaion they come with.
        lines = self.getlines()
        stream = ' '.join(lines)
        allwords = re.split('\s+', stream)
        ''' don't need to worry about empty string, since we stripped all
        the lines in Poems.getlines. '''
        return allwords
        """
        textWithoutTitleAuthorLine = self.getpoemtext()
        # tokenizedtext = nltk.word_tokenize(textWithoutTitleAuthorLine)
        #   This was eschewed since nltk.word_tokenize would do the following:
        #       "I'll" |--> ['I', "'ll"]
        nopunctAposOK = re.sub('['+punctnoapos+']',
                               ' ',
                               textWithoutTitleAuthorLine)
        #tokenizedtextnopunct = [word for word in tokenizedtext
        #                        if word not in punct]
        #   This was eschewed since it would not remove text such as '--'. 
        tokenizedtextnopunct = nopunctAposOK.split()
        return tokenizedtextnopunct

    def getnontrivialwords(self):
        ''' Method for obtaining the non-trivial words in 'words'
        attribute of Poems instance 'self'. See documentation on Poems
        method getallwords() for the author's complaints on how the
        method at hand could be improved. 

            returns: nontrivialwords (dict) whose keys are the non-trivial
        words in the Poems instance 'self', and whose values are the
        frequencies of word appearances in that Poems instance. For
        example, if the word 'taxi' appears four times in the text of 
        Poems instance 'self', then executing
        'print nontrivialwords['taxi']' should return 4. Note that keys
        will necessarily be made lowercase. 
        '''
        try:
            nontrivialwords = self.words
        except AttributeError:
            allwords = [word.lower() for word in self.getallwords()]
            allwords_contractionsexpanded = set()
            for word in allwords:
                if word in allwords_contractionsexpanded:
                    continue
                else:
                    if word in CONTRACTION_MAP:
                        allwords_contractionsexpanded.update(\
                            CONTRACTION_MAP[word].split())
                    else:
                        allwords_contractionsexpanded.add(word)
            englishstopwords = stopwords.open('english').read()[:-1].split('\n')
            nontrivialwords = {word:allwords.count(word)
                               for word in allwords_contractionsexpanded
                               if word not in englishstopwords}
        finally:
            return nontrivialwords

    def getnontrivialnouns(self):
        ''' Method for obtaining the non-trivial nouns in 'words'
        attribute of Poems instance 'self'. See documentation on Poems
        method getallwords() for the author's complaints on how the
        method at hand could be improved. 

            returns: nontrivialnouns (dict) whose keys are the non-trivial 
        nouns in the Poems instance 'self', and whose values are the
        frequencies of word appearances in that Poems instance. For
        example, if the word 'taxi' appears four times in the text of 
        Poems instance 'self', then executing
        'print nontrivialwords['taxi']' should return 4. Note that keys
        will necessarily be made lowercase.

        NOTES:

        There is a massive assumption made in this function. That assumption
        is that if a word (i.e., string) shows up in wordnet as a noun,
        then it is counted as a noun in our Poems class. 
        '''
        try:
            nontrivialnouns = self.nouns
            # in case already defined
        except AttributeError:
            try:
                nontrivialwords = self.words
            except AttributeError:
                nontrivialwords = self.getnontrivialwords()
                # Do this in case we end up definining nouns before words
            finally:
                """
                # second stab
                # idea: use the lesk tokenizer in-line to disambiguate
                # whether a word is a noun or not.

                # should relegate to a function isnoun? 

                lines = self.getlines()
                for word in nontrivialwords:
                    for line in lines:
                        splitline = line.lower().split()
                        if word in line:
                            mysyn = lesk(nltk.word_tokenize(line.lower()), word)
                            if mysyn.pos()=='n':
                                # do something
                        else:
                            continue
                """
                nontrivialnouns = {}
                for word in nontrivialwords:
                    try:
                        firstsynset = wn.synsets(word, pos='n')[0]
                        # the above line is the 'greedy' part. 
                        nontrivialnouns[word]=nontrivialwords[word]
                    except IndexError:
                        continue
        finally:
            return nontrivialnouns
        
    def getpoemtext(self):
        ''' Method for obtaining the poem text less the POEM: AUTHOR: line.
        '''
        return Poems.getpoeminfo(self.text)[2]
        
    @classmethod
    def smallestPoem(cls):
        ''' Static Method for obtaining the ID of the Poems instance with the
        smallest number of lines (according to the Poems.getnumberLines()
        function). 

            input: cls (class; intended to be Poems)
            returns: poemId (int) corresponding to the Poems instance with
        the least number of lines of all Poems instances currently defined.
        '''
        smallest = cls._allPoems[0]
        for p in cls._allPoems:
            if p.numberLines < smallest.numberLines:
                smallest = p
        return smallest.poemId

    @staticmethod
    def getPoem(ID):
        ''' Method for getting a Poem instance by its ID.

            input: ID (int) referring to a Poems instance
            returns: Poems instance whose poemId is the same as input ID '''
        for Poem in Poems._allPoems:
            if Poem.poemId == ID:
                return Poem
        else:
            raise IndexError('ID not found in Poems.')
        pass

    @staticmethod
    def printPoembyId(ID):
        ''' input: ID (int) referring to a Poems instance
            returns: nothing; simply prints out the poem text to the
        console and then passes.
        '''
        print Poems.getPoem(ID)
        pass
    
    @staticmethod
    def split_up_poems(raw_text):
        ''' Static Method which processes a string containing a number of
        poems. I am assuming here that all poems are separated by the
        'POEM: ... AUTHOR: ...\n' line structure that is inherent in
        Poems_new_2018.txt. 

            input: raw_text (str) containing all poems
            returns: list containing individual poems
        '''
        splitup = re.split('(POEM:.+AUTHOR:.+)', raw_text)
        splitup[1] = ''.join([splitup[0],splitup[1]])
        ''' need to join up information from before the first split with
        the first split itself. In the case of the file given, this really
        does't do much. But darnit if I don't like a bit of generality in
        my code. '''
        splitup.pop(0) # get rid of (now) extraneous first element
        out = [''.join([splitup[i],splitup[i+1]])
               for i in range(0,len(splitup),2)]
        return out

    @staticmethod
    def getpoeminfo(singletext):
        ''' Method for getting poem information from a piece of poetry. 

            input: singletext (str) containing raw text from ONE poem
            returns: out (list) containing (0) poem title, (1) author,
                     and (2) text of the poem, stripped of newlines at both
                     beginning and end. 
        '''
        splitup = re.split('(POEM:.+AUTHOR:.+)', singletext)
        infoline = splitup[1]
        title,author = re.split('AUTHOR:.+', infoline[5:])
        strippedtext = splitup[2].strip('\n')
        return [title, author, strippedtext]
    
    def __lt__(self, other):
        ''' Method to sort Poems instances. It sorts based on the sentiment
        score. '''
        return self.sentiment < other.sentiment

    def __str__(self):
        ''' Method to define what should happen if we call "print P", where
        P is a Poems instance. '''
        return self.text
    
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

    -----Discuss strategy-----

    When initializing a Nouns instance, we check to see if wordnet
    recognizes the input 'noun' as an actual NOUN. If not, a ValueError
    is raised, and initialization of the Nouns instance is aborted.

    Note that the private variable Nouns._allNouns has a different
    structure than Poems._allPoems. The latter is a list of Poems
    instances, whereas the former is a dictionary whose keys are nouns
    (strings) and values are frequencies (ints) of how often the noun
    appears in all Poems instances. 
    '''

    _allNouns = {}
    _curNounId = 1
    def __init__(self, noun):
        ''' input: noun (str). Arguments passed that are not actual nouns
        in wordnet will cause a ValueError to be raised.
            returns: Nouns instance will all attributes described above.
        ''' 
        try:
            firstsynset = wn.synsets(noun, pos='n')[0]
        except IndexError:
            try:
                firstsynset = wn.synsets(wn.morphy(noun), pos='n')[0]
            except IndexError:
                raise ValueError('Input \'{}\' to Nouns(...) was not found to be a noun.'.format(noun))
        finally:
            self.synset = firstsynset
            self.definition = firstsynset.definition()
            self.noun = noun
            if self.noun not in Nouns._allNouns:
                self.nounId = Nouns._curNounId
                Nouns._curNounId +=1
                Nouns._allNouns[self.noun] = self.nounId
            else:
                self.nounId = Nouns._allNouns[self.noun]
            self.pidlist = [p.poemId for p in Poems._allPoems
                            if self.noun in p.nouns]
            self.frequency = sum([Poems.getPoem(pid).nouns[self.noun]
                                  for pid in self.pidlist])
        pass

def wordtrain(train):
    ''' input: train (str) whose first word (before whitespace) is not
    contained in any of the words in any of the poems in the Poems classes
        returns: train (str) of <100 characters where the last character
    of each word matches the first character of the next word in the train
    '''
    trainwords = train.split()
    firstword = trainwords[0]
    if len(train)>=100:
        raise ValueError('Length of wordtrain should not be >=100 characters.')
    elif firstword in Poems._allPoemswords:
        raise ValueError('Beginning word of the train \'{}\' was found in \
                        Poem {}.'.format(firstword,p.poemId))
    else:
        char = trainwords[-1][-1]
        for word in Poems._allPoemswords:
            if (word[0]==char
                and len(train+' '+word) <=99
                and word not in trainwords):
                return wordtrain(train + ' ' + word)
        return train

    
def Problem5(mystr):
    ''' input: mystr (str)
        returns: boolean (TRUE or FALSE) depending on whether the string
    mystr satisfies:
            i)   length of mystr is >= 7 but <10
            ii)  mystr contains at least one punctuation character
            iii) mystr contains at least one uppcercase character
            iv)  mystr is not contained in any of the Poems words
    '''

    ''' NOTE: this function is basically superfluous, since the words
    attribute of any of the Poems instances ignores capitalizationa and
    punctuation. *sigh*
    '''
    i = (len(mystr) >= 7 and len(mystr) < 10)
    ii = any([p in mystr for p in punct])
    iii = mystr.lower() != mystr
    iv = any([mystr.lower() in poem.words for poem in Poems._allPoems])
    # for iv, need to make mystr lowercase, since all words are stored lc.
    if not i:
        print 'Input {} has len(...)<7 or len(...)>=10.'.format(mystr)
        return False
    elif not ii:
        print 'Input {} contains no punctuation.'.format(mystr)
        return False
    elif not iii:
        print 'Input {} does not contain an uppercase character.'.format(mystr)
        return False
    elif not iv:
        print 'Input {} not found in any Poems instance.'.format(mystr)
        return False
    else:
        return True


# read in and process the file Poems_new_2018.txt: 

cwd = os.getcwd() 
poemsfile = cwd + '\\Poems_new_2018.txt'
myPoems = open(poemsfile, 'r')
#print myPoems.read()
Poemstext = myPoems.read()
myPoems.close()
allpoemtexts = Poems.split_up_poems(Poemstext)
for poemtext in allpoemtexts:
    title, author, strippedtext = Poems.getpoeminfo(poemtext)
    # won't actually used stripped text in this case.
    p = Poems(title, author, poemtext)
for p in Poems._allPoems:
    for noun in p.nouns:
        n = Nouns(noun)

# tests of wordtrain() function:
print wordtrain('train')
print wordtrain('lobe') 
