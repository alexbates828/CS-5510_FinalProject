'''

project stub

State any assumptions you make here. Note these should not contradict
any aspect of the project description.

You may create additional attributes for either class as needed for your assignment.

You may need to use regular expressions. While we will do this in class,
you may want to get a head start and look at:

http://www.tutorialspoint.com/python/python_reg_expressions.htm

'''


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
    
    '''
    
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

    


    
