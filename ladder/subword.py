import doctest

with open ('words.txt') as f:
    ALL_WORDS = {i.strip() for i in f}

def subwords(word):
    """
    >>> result = subwords('cat')
    >>> expected = {'cat', 'at', 'act'}
    >>> result == expected
    True
    """
    return {w for w in helper(word) if w in ALL_WORDS}

def helper(word):
    """
    >>> result = set(helper("cat"))
    >>> expected = {'', 'c', 'a', 't', 
    ...             'ca', 'ct', 'ac', 'at', 'tc', 'ta', 
    ...             'cat', 'cta', 'tca', 'tac', 'atc', 'act'}
    >>> result == expected
    True
    """

    if not word:
        yield ''
        return
    
    #out = set()
    first = word[0]
    rest = word[1:]

    for w in helper(rest):
        yield w
        for ix in range(len(w) + 1):
            yield (w[ix:] + first + w[:ix])
    #return out


if __name__ == "__main__":
    doctest.testmod(verbose = True)
    print(subwords("artichokes"))