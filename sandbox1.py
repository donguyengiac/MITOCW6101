Cap = 47E-9
R1 = 1000
notes = {
    "C1" : 32.70 ,
    "C#1/Db1" : 34.65 ,
    "D1" : 36.71 ,
    "D#1/Eb1" : 38.89 ,
    "E1" : 41.20 ,
    "F1" : 43.65 ,
    "F#1/Gb1" : 46.25 ,
    "G1" : 49.00 ,
    "G#1/Ab1" : 51.91 ,
    "A1" : 55.00 ,
    "A#1/Bb1" : 58.27 ,
    "B1" : 61.74 ,
    "C2" : 65.41 ,
    "C#2/Db2" : 69.30 ,
    "D2" : 73.42 ,
    "D#2/Eb2" : 77.78 ,
    "E2" : 82.41 ,
    "F2" : 87.31 ,
    "F#2/Gb2" : 92.50 ,
    "G2" : 98.00 ,
    "G#2/Ab2" : 103.83 ,
    "A2" : 110.00 ,
    "A#2/Bb2" : 116.54 ,
    "B2" : 123.47 ,
    "C3" : 130.81 ,
    "C#/Db3" : 138.59 ,
    "D3" : 146.83 ,
    "D#/Eb3" : 155.56 ,
    "E3" : 164.81 ,
    "F3" : 174.61 ,
    "F#/Gb3" : 185.00 ,
    "G3" : 196.00 ,
}

keys = list(notes.keys())
keys.reverse()

def formula(freq):
    r = (1.44/(freq*Cap) - R1 )/ 2
    return round(r, 1)

def convert(Res):
    list_of_R = [100, 150, 200, 220, 270, 330, 470, 510, 680, 1000, 2000, 2200, 3300, 4700, 5100, 6800, 10000, 20000, 47000, 51000, 68000, 100000, 220000, 300000, 470000, 680000]
    list_of_R.reverse()
    out = []
    R = Res
    idx = 0
    while idx in range(len(list_of_R)):
        resistor = list_of_R[idx]
        
        if R < 900: return out
        if R // resistor >= 1:
            #print(resistor)
            if R-resistor < 100: 
                idx += 1
                #print("nah")
                continue
            R = R - resistor
            ans = str(resistor)
            if resistor >= 1000: 
                ans = str(resistor/1000) + "k"
            out.append(ans)
            idx = 0
        idx += 1

        

initialR= 0
print (f"resistance 0 {formula(notes["G3"])}")
for idx in range(len(keys)):
    key = keys[idx]
    ans = round(formula(notes[key]) - initialR, 1)
    if (idx == 0): 
        initialR = formula(notes[key])
    
    
    #print(f"{key}, total R: {formula(notes[key])}, difference: {ans}, resistors: {convert(ans)}")
    print(f"{key}, resistors: {convert(ans)}")
    if len(convert(ans)) > 3: print(ans)


#print(convert(22085.7))



