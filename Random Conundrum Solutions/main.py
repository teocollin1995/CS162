import itertools
from sys import argv


def cands(inputs):
    """
    Finds all permutations with more than 4 characters of a list of characters
    :arg List of characters
    :return list of strings
    """
    # The below could probably be simplified a bit....
    return map(''.join, list(itertools.chain.from_iterable([ map (list, (itertools.permutations(inputs, x))) for x in range(4, len(inputs)+1)])))

def dict_make():
    """
    Creates a dictionary of all words greater than length 4
    :args None
    :return A dictionary
    """
    f = open('words.txt','r')
    dict1 = f.read().splitlines()
    return filter(lambda z:len(z) >= 4, dict1)

def main():
    """
    Solves a conundrum as specified here: http://brick.cs.uchicago.edu/Courses/CMSC-16200/2015/pmwiki/pmwiki.php/SunWooPark/RandomConundrumSolutions
    :arg None
    :return None
    """
    string = argv[1] # The 2nd command line argument.
    possible = cands(string)
    dictionary = dict_make()
    results = [possible[x] for x in xrange(0, len(possible)) if possible[x] in dictionary]
    if len(results) == 0:
        print "No Solution"
        return ()
    else:
        for x in range(0, len(results)):
            print results[x]
    return ()

main()
