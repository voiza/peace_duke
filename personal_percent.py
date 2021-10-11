#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import numpy as np
from typing import List, Tuple

def lerp(a, b, x):
    return (1 - x) * a + x * b

def cirp(a, b, x):
    "cosine interpolation"
    ft = x * np.pi
    f = (1 - np.cos(ft)) / 2
    return a*(1-f) + b*f

def scirp(v0, v1, v2, x):
    "square cosine interpolation"
    return cirp(cirp(v0, v1, 0.5+x*0.5), cirp(v1, v2, x*0.5), x)

def get_digest(prefix: str, n: int) -> str:
    return hashlib.sha256(f"{prefix}{int(n)}".encode('ASCII')).hexdigest()

def digest_to_01(digest: str) -> float:
    v = int(digest, 16)/2**256
    return v

def get_nth_value(signature, n: float) -> float:
    d = int(n)
    x = n - d

    v0 = digest_to_01(get_digest(signature, d))
    v1 = digest_to_01(get_digest(signature, d+1))

#    ret = lerp(v0, v1, x)
    ret = cirp(v0, v1, x)

#    v2 = digest_to_01(get_digest(signature, d+2))
#    ret = scirp(v0, v1, v2, x)

    return ret

class PersonalPercent(object):
    Frequency = int             #larger is shorter period
    AmplitudeInverse = int      #larger is less impactful
    Harmonic = Tuple[Frequency, AmplitudeInverse]
    Harmonics = List[Harmonic]

    def __init__(self, harmonics: Harmonics, pepper: str, id: int):
        self.signature=get_digest(pepper, id)
        self.harmonics = harmonics
        self.max = 0

    def get(self, t: float) -> float:
        ret = 0
        mul = 0
        for z, h in enumerate(self.harmonics):
            value = get_nth_value(self.signature+f"{z}th", t*h[0])
            ret += value/h[1]
            mul += 1/h[1]
        ret /= mul

        self.max = max(self.max, ret)

        return ret

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    PEPPER="some-static-garbage"
    ID=75635000

    #harmonics = [13,37] #~25 oscilations per 1t, max=0.99572
    #harmonics = [3,11] #~5 oscilations per 1t, max=0.99067
    harmonics = [3,13,37]
    #harmonics = [2,51] #~3 oscilations per 1t, max=0.99067
    t = np.linspace(0, 10, 60*60)

    pp = PersonalPercent([(x,x) for x in harmonics], PEPPER, ID)
    value = np.vectorize(pp.get)(t)

    plt.plot(t, value)
    plt.title(harmonics)
    plt.ylabel('%%')
    plt.xlabel('Time(t)')
    plt.show()
