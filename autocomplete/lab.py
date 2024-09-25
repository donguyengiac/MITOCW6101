"""
6.101 Lab:
Autocomplete
"""

# NO ADDITIONAL IMPORTS!
import doctest
import os.path
from text_tokenize import tokenize_sentences
import test

TEST_DIRECTORY = os.path.dirname(__file__)


class PrefixTree:
    def __init__(self):
        self.value = None
        self.children = {}

    def test(self):
        """
        >>> t = PrefixTree()
        >>> t['bat'] = True
        >>> t['bar'] = True
        >>> t['bark'] = True
        >>>
        >>> t['bat']
        True
        >>> t['something']
        Traceback (most recent call last):
            ...
        KeyError
        >>>
        >>> t['bark'] = 20
        >>> t['bark']
        20
        >>>
        >>> for i in t:
        ...    print(i)
        ('bat', True)
        ('bar', True)
        ('bark', 20)
        >>>
        >>> del t['bar']
        >>>
        >>> for i in t:
        ...    print(i)
        ('bat', True)
        ('bark', 20)
        """
        
    def __setitem__(self, key, value):
        """
        Add a key with the given value to the prefix tree,
        or reassign the associated value if it is already present.
        Raise a TypeError if the given key is not a string.

        """
        if not isinstance(key, str): raise TypeError
        if len(key) == 0:
            self.value = value
        else:
            char = key[0]
            rest = key[1:]
            if char in self.children:
                self.children[char][rest] = value
            else:
                nextTree = PrefixTree()
                nextTree[rest] = value
                self.children.update({char: nextTree})

    def __getitem__(self, key):
        """
        Return the value for the specified prefix.
        Raise a KeyError if the given key is not in the prefix tree.
        Raise a TypeError if the given key is not a string.

        """
        if not isinstance(key, str): raise TypeError
        if len(key) == 0:
            if self.value is None: raise KeyError
            return self.value
        char = key[0]
        rest = key[1:]
        if char not in self.children: raise KeyError
        return (self.children[char])[rest]

    def get_tree_from(self, key):
        if len(key) == 0: return self
        char = key[0]
        rest = key[1:]
        if char not in self.children: 
            raise KeyError
        return self.children[char].get_tree_from(rest)
    
    def __delitem__(self, key):
        """
        Delete the given key from the prefix tree if it exists.
        Raise a KeyError if the given key is not in the prefix tree.
        Raise a TypeError if the given key is not a string.
        """
        try:
            self[key]
        except KeyError: raise KeyError
        except TypeError: raise TypeError
        self[key] = None
    def __contains__(self, key):
        """
        Is key a key in the prefix tree?  Return True or False.
        Raise a TypeError if the given key is not a string.
        """
        try:
            self[key]
            return True
        except KeyError:
            return False
        except TypeError:
            raise TypeError

    def __iter__(self):
        """
        Generator of (key, value) pairs for all keys/values in this prefix tree
        and its children.  Must be a generator!
        """
        for key in self.children:
            if self.children[key].value is not None: yield (key, self.children[key].value)
            for tuple in self.children[key]:
                yield (key + tuple[0], tuple[1])
        
        #raise NotImplementedError



def word_frequencies(text):
    """
    Given a piece of text as a single string, create a prefix tree whose keys
    are the words in the text, and whose values are the number of times the
    associated word appears in the text.

    >>> T = word_frequencies("Given a piece of text as a single string, create a prefix tree whose keys are the words in the text, and whose values are the number of times the associated word appears in the text.")
    >>> T['a'] 
    3
    >>> T['text']
    3
    >>> T['are']
    2
    """
    sentences = tokenize_sentences(text)
    tree_out = PrefixTree()
    for sentence in sentences:
        words = sentence.split()
        for word in words:
            if word in tree_out:
                tree_out[word] += 1
            else:
                tree_out[word] = 1
    return tree_out

    


def autocomplete(tree, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is not a string.

    

    """
    if not isinstance(prefix, str): raise TypeError
    frequency_list = []
    try:
        if prefix in tree: 
            frequency_list.append((prefix, tree[prefix]))
        for tuple in tree.get_tree_from(prefix):
            frequency_list.append(tuple)
        frequency_list.sort(reverse=True, key = lambda x: x[1])
        #print(frequency_list)
        out = []
        for i in frequency_list[:max_count]:
            if i[0] != prefix:
                out.append(prefix + i[0])
            else:
                out.append(i[0])
        return out
    except KeyError: return []
    raise NotImplementedError

def insertion_list(tree, word):
    """
    return list of tuple of new words and their frequencies
    """
    out = []
    
    for idx in range(len(word)+1):
        for c in list(map(chr,range(ord('a'), ord('z')+1))):
            new_word = word[:idx] + c + word[idx:]
            if new_word in tree:
                out.append((new_word, tree[new_word]))
    return out

def deletion_list(tree, word):
    """
    return list of tuple of new words and their frequencies
    """
    out = []
    
    for idx in range(len(word)):
        new_word = word[:idx] + word[idx+1:]
        if new_word in tree:
            out.append((new_word, tree[new_word]))
    return out

def replacement_list(tree, word):
    """
    return list of tuple of new words and their frequencies
    """
    out = []
    
    for idx in range(len(word)):
        for c in list(map(chr,range(ord('a'), ord('z')+1))):
            new_word = word[:idx] + c + word[idx+1:]
            if new_word in tree and new_word != word:
                out.append((new_word, tree[new_word]))
    return out

def transposition_list(tree, word):
    """
    return list of tuple of new words and their frequencies
    """
    out = []

    for idx in range(len(word)-1):
        new_word = word[:idx] + word[idx+1] + word[idx] + word[idx+2:]
        #print(new_word)
        if new_word in tree and new_word != word:
            print(new_word)
            out.append((new_word, tree[new_word]))
    return out

def autocorrect(tree, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    """
    autocomplete_list = autocomplete(tree, prefix, max_count)
    out_set = set(autocomplete_list)
        #check insertion list, deletion list, replacement list, transpose list
        #find elements with the most frequency
        #add to autocomplete list
    insert_list = insertion_list(tree, prefix)
    delete_list = deletion_list(tree, prefix)
    replace_list = replacement_list(tree, prefix)
    transpose_list = transposition_list(tree, prefix)
    long_list = insert_list + delete_list + replace_list + transpose_list
    long_list.sort(reverse=True, key=lambda x: x[1])
    #print(long_list)
    if max_count is not None and len(autocomplete_list) < max_count:
        for i in long_list:
            if len(out_set) < max_count:
                out_set.add(i[0])
    else:
        if max_count is None: 
            for i in long_list:
                out_set.add(i[0])
    
    return list(out_set)
    raise NotImplementedError

def process(pattern):
    if len(pattern) == 0: return ""
    out = pattern[0]
    for c in pattern[1:]:
        if c == "*" and out[len(out)-1] == "*":
            continue
        out = out + c
    return out

def word_filter(tree, pattern):
    """
    Return list of (word, freq) for all words in the given prefix tree that
    match pattern.  pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """
    """normal = True
    for c in pattern:
        if c == '?' or c == '*': normal = False
    if normal: 
        try:
            return [(pattern, tree[pattern])]
        except KeyError: return[]
    """
    pattern = process(pattern)
    print(pattern)
    def helper(treeNode, index, string):
        #print(string)
        if index >= len(pattern): 
            if treeNode.value is not None:
                yield (string, treeNode.value)
            else: yield None
            return
        char = pattern[index]
        if char == "?":
            for c in treeNode.children:
                yield from helper(treeNode.children[c], index+1, string+c)
        elif char == "*":
            question = False
            if index+1 >= len(pattern): next_char = None
            elif pattern[index+1] == '?': 
                next_char = None
                question = True
            else: next_char = pattern[index+1] #lookahead, will need to check for out of range later
            #print(next_char)
            for node, chunk in find_next(treeNode, next_char, "", question): #find_next returns node whose next_char points to, and chunk including next_char
                #print(chunk)
                yield from helper(node, index+1, string+chunk)
        else:
            if char in treeNode.children:
                yield from helper(treeNode.children[char], index+1, string+char)
            else: 
                yield None
                return
    
    return list({i for i in helper(tree, 0, "") if i is not None})
        
def find_next(treeNode, char, chunk, question = False):
    #print(chunk)
    if char is None:
        if treeNode.value is not None or question:
            #print('yield')
            yield (treeNode, chunk)

    elif char in treeNode.children:
        yield (treeNode, chunk)

    for c in treeNode.children:
        yield from find_next(treeNode.children[c], char, chunk+c, question)
    

# you can include test cases of your own in the block below.
if __name__ == "__main__":
    #doctest.testmod()
    #T = PrefixTree()
    #T['bat'] = 7
    #T['bar'] = 3
    
    """print(T.value)
    print (T.children)
    for nextTree in T.children.items():
        print(nextTree[0])
        for nextNextTree in nextTree[1].children.items():
            print(nextNextTree[0])
            for nextNextNextTree in nextNextTree[1].children.items():
                print(nextNextNextTree[0])
                print(nextNextNextTree[1].value)
    """
    #print(T['bat'])
    """T = word_frequencies("bat bat bark bar")
    
    print(autocomplete(T, "ba", 2))

    t = word_frequencies("cat car carpet")
    print(autocomplete(t, 'ce', 3))"""
    
    #t = word_frequencies("cats cattle hat care cats cars act at chat crate act cans cars act")
    #t = word_frequencies("man mat mattress map me met a man a a a map man met")

    #print(word_filter(t, "**at**"))
    #test.test_autocorrect_big()

    with open(os.path.join(TEST_DIRECTORY, 'testing_data', 'frankenstein.txt'), encoding='utf-8') as f:
        text = f.read()
    w = word_frequencies(text)
    expected = test.read_expected('frank_filter_%s.pickle' % (3, ))
    print(word_filter(w, "**ing**"))
    print()
    print(expected)
    