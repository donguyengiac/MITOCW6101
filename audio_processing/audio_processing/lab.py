"""
6.101 Lab:
Audio Processing
"""

import wave
import struct

# No Additional Imports Allowed!


def backwards(sound):
    samples = sound["samples"][:]
    # print(sound['samples'])
    samples.reverse()
    # print(sound['samples'])
    out = {"rate": sound["rate"], "samples": samples}
    return out
    raise NotImplementedError


def mix(sound1, sound2, p):
    if sound1["rate"] != sound2["rate"]:
        return None
    out = {"rate": sound1["rate"]}
    sampleLength = max(len(sound1["samples"]), len(sound2["samples"]))
    samples = [None] * sampleLength
    for i in range(sampleLength):
        try:
            samples[i] = p * sound1["samples"][i] + (1 - p) * sound2["samples"][i]
        except:
            try:
                samples[i] = p * sound1["samples"][i]
            except:
                samples[i] = (1 - p) * sound2["samples"][i]

    out["samples"] = samples
    return out
    raise NotImplementedError


def convolve(sound, kernel):
    sampleLength = len(sound['samples']) + len(kernel) - 1
    out = {
        'rate': sound['rate']
    }
    samples = [0] * sampleLength
    for i in range(0, len(kernel)):
        if (kernel[i] != 0):
            for j in range(0, len(sound['samples'])):
                samples[i+j] += sound['samples'][j]*kernel[i]
    out['samples'] = samples
    return out
    raise NotImplementedError

def echo_kernel(delay, length, scale):
    kernel = [0] * (length + 1)
    for i in range(0, length+1, delay):
        kernel[i] = scale**(i/delay)
    return kernel
    

def echo(sound, num_echoes, delay, scale):
    sample_delay = round(delay*sound['rate'])
    added_length = num_echoes*sample_delay
    kernel = echo_kernel(sample_delay, added_length, scale)
    #print(kernel)
    out = convolve(sound, kernel)
    return out
    raise NotImplementedError


def pan(sound):
    out = {'rate': sound['rate']}
    left_samples = sound['left'][:]
    right_samples = sound['right'][:]
    length = len(left_samples)
    for i in range(length):
        right_samples[i] *= (i/(length-1))
        left_samples[i] *= 1-(i/(length-1))
    out['left'] = left_samples
    out['right'] = right_samples
    return out
    raise NotImplementedError


def remove_vocals(sound):
    out = {'rate': sound['rate']}
    samples = [0] * len(sound['left'])
    for i in range(len(sound['left'])):
        samples[i] = sound['left'][i] - sound['right'][i]
    out['samples'] = samples
    return out
    raise NotImplementedError


def bass_boost_kernel(n_val, scale=0):
    """
    Construct a kernel that acts as a bass-boost filter.

    We start by making a low-pass filter, whose frequency response is given by
    (1/2 + 1/2cos(Omega)) ^ n_val

    Then we scale that piece up and add a copy of the original signal back in.
    """
    # make this a fake "sound" so that we can use the convolve function
    base = {"rate": 0, "samples": [0.25, 0.5, 0.25]}
    kernel = {"rate": 0, "samples": [0.25, 0.5, 0.25]}
    for i in range(n_val):
        kernel = convolve(kernel, base["samples"])
    kernel = kernel["samples"]

    # at this point, the kernel will be acting as a low-pass filter, so we
    # scale up the values by the given scale, and add in a value in the middle
    # to get a (delayed) copy of the original
    kernel = [i * scale for i in kernel]
    kernel[len(kernel) // 2] += 1

    return kernel


# below are helper functions for converting back-and-forth between WAV files
# and our internal dictionary representation for sounds


def load_wav(filename, stereo=False):
    """
    Given the filename of a WAV file, load the data from that file and return a
    Python dictionary representing that sound
    """
    file = wave.open(filename, "r")
    chan, bd, sr, count, _, _ = file.getparams()

    assert bd == 2, "only 16-bit WAV files are supported"

    out = {"rate": sr}

    if stereo:
        left = []
        right = []
        for i in range(count):
            frame = file.readframes(1)
            if chan == 2:
                left.append(struct.unpack("<h", frame[:2])[0])
                right.append(struct.unpack("<h", frame[2:])[0])
            else:
                datum = struct.unpack("<h", frame)[0]
                left.append(datum)
                right.append(datum)

        out["left"] = [i / (2**15) for i in left]
        out["right"] = [i / (2**15) for i in right]
    else:
        samples = []
        for i in range(count):
            frame = file.readframes(1)
            if chan == 2:
                left = struct.unpack("<h", frame[:2])[0]
                right = struct.unpack("<h", frame[2:])[0]
                samples.append((left + right) / 2)
            else:
                datum = struct.unpack("<h", frame)[0]
                samples.append(datum)

        out["samples"] = [i / (2**15) for i in samples]

    return out


def write_wav(sound, filename):
    """
    Given a dictionary representing a sound, and a filename, convert the given
    sound into WAV format and save it as a file with the given filename (which
    can then be opened by most audio players)
    """
    outfile = wave.open(filename, "w")

    if "samples" in sound:
        # mono file
        outfile.setparams((1, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = [int(max(-1, min(1, v)) * (2**15 - 1)) for v in sound["samples"]]
    else:
        # stereo
        outfile.setparams((2, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = []
        for left, right in zip(sound["left"], sound["right"]):
            left = int(max(-1, min(1, left)) * (2**15 - 1))
            right = int(max(-1, min(1, right)) * (2**15 - 1))
            out.append(left)
            out.append(right)

    outfile.writeframes(b"".join(struct.pack("<h", frame) for frame in out))
    outfile.close()


if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place to put your
    # code for generating and saving sounds, or any other code you write for
    # testing, etc.

    # here is an example of loading a file (note that this is specified as
    # sounds/hello.wav, rather than just as hello.wav, to account for the
    # sound files being in a different directory than this file)

    mystery = load_wav("sounds/mystery.wav")
    chord = load_wav("sounds/chord.wav")
    meow = load_wav("sounds/meow.wav")
    synth = load_wav("sounds/synth.wav")
    water = load_wav("sounds/water.wav")
    ice = load_wav("sounds/ice_and_chilli.wav")
    chickadee = load_wav("sounds/chickadee.wav")
    car = load_wav("sounds/car.wav", stereo=True)
    mountain = load_wav("sounds/lookout_mountain.wav", stereo = True)
    abba = load_wav("sounds/abba1.wav", stereo = True)
    # print(hello)
    # write_wav(backwards(mystery), 'mystery_reversed.wav')
    write_wav(remove_vocals(abba), "abba_karaoke.wav")
    
