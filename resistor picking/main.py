catalog = [100, 150, 200, 220, 270, 330, 470, 510, 680, 
           1E3, 2E3, 2.2E3, 3.3E3, 4.7E3, 5.1E3, 6.8E3, 
           10E3, 20E3, 47E3, 51E3, 68E3, 
           100E3, 220E3, 300E3, 470E3, 680E3, 1E6]

"""
Approach:
- function takes in target value, lower & upper acceptable levels (tuple). if range not inputted then assumed to be 1%. 
- if found within range, returns resistor arrangement: parallel is tuple, series is list
- for example: R1 // (R2 + R3) = (R1, [R2, R3])
               R1 // R2 // R3 = (R1, R2, R3) = (R1, (R2, R3))
               R1 + R2 + R3: [R1, [R2, R3]] = [R1, R2, R3]
- permutations: [R1, R2, R3] = [R2, R1, R3]
- keep a list of checked states.
"""

def found(target, range):
    #print(target)
    best = -1
    target = round(target)
    for R in catalog: 
        #print("R", R)
        if R == target: return R
        if R > round(range[0]) and R < round(range[1]): best = R
        if R > round(range[1]): break
    if best != -1: return best
    return None

def findR(target, range = None):
    #print(target)
    if range is None: 
        lower = target*.99
        higher = target*1.01
        range = (lower, higher)

    found_value = found(target, range)
    if found_value is not None: return found_value

    for R in catalog:
        series = findR(target-R, (range[0]-R, range[1]-R))
        #print("series", series)
        if series is not None: return [R, series]
        parallel = findR(target * R / (R-target), (range[0] * R / (R-range[0]), range[1] * R / (R-range[1])))
        if parallel is not None: return (R, parallel)
    
    return None

print(findR(1550))



