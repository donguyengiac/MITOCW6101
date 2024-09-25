import doctest
def mixtape(songs, target):
    """
    >>> songs = {'A': 5, 'B':10, 'C':6, 'D':2}
    >>> mixtape(songs, 11) == {'A', 'C'}
    True
    >>> mixtape(songs, 1000) is None
    True
    """
    agenda = [set()]
    
    while agenda:
        option = agenda.pop()
        if sum(songs[i] for i in option) == target: return option
        if sum(songs[i] for i in option) > target: continue
        for song in songs:
            if song not in option:
                agenda.append(option | {song})
    return None






if __name__ =="__main__":
    doctest.testmod()