#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import hashlib
import numpy as np
from typing import List, Tuple
import matplotlib.pyplot as plt

from datetime import datetime

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

    def __init__(self, harmonics: Harmonics, seed: str, id: int):
        self.signature=get_digest(seed, id)
        self.harmonics = harmonics
        self.max = 0
        self.div = 60*60*10 # frequency reduction factor

        self.img_dpi=120
        self.img_size_inches=(6,5)

    def get_ts(self, ts: int) -> float:
        return self.get_float(ts/self.div)

    def get_float(self, t: float) -> float:
        ret = 0
        mul = 0
        for z, h in enumerate(self.harmonics):
            value = get_nth_value(self.signature+f"{z}th", t*h[0])
            ret += value/h[1]
            mul += 1/h[1]
        ret /= mul

        self.max = max(self.max, ret)

        return ret

    def _fig2bytes(self, fig):
        buf = io.BytesIO()
        fig.savefig(buf)
        buf.seek(0)
        return buf
    
    def get_image(self, ts: int, name: str, scale: int=60, shift: int=48):
        t = ts / self.div
        v = self.get_float(t)

        min_x = t-(scale+shift)/self.div/2
        max_x = t+(scale-shift)/self.div/2
        ls = np.linspace(min_x, max_x, 200)
        value = np.vectorize(lambda i: self.get_float(i))(ls)
        plt.figure(figsize=self.img_size_inches, dpi=self.img_dpi)
        plt.plot(ls, value)
        plt.plot(t, v, 'r+')

        plt.title(name)

        delta = (max_x-min_x)/10
        locs = np.arange(min_x, max_x+delta, delta)
        lbs = (datetime.fromtimestamp(loc*self.div).strftime("%H:%M:%S") for loc in locs)
        plt.xticks(locs, lbs, rotation=25)

        locs, labels = plt.yticks()
        plt.yticks(locs, [f"{percent*100:.1f}%" for percent in locs])

        plt.grid(linestyle=':', linewidth=1)

        fig = plt.gcf()
        bytes = self._fig2bytes(fig)
        plt.close()
        return bytes

def __example():
    from PIL import Image

    SEED="some-static-garbage"
    ID=75635000

    harmonics = (3,13,37)
    
    pp = PersonalPercent([(x,x) for x in harmonics], SEED, ID)
    for a in [0,5*60,10*60]: #example of 5-minutes progress in 3 iterations
        import time
        ts = 1634048870+350435 #time.time()
        x = pp.get_image(ts+a, "me", scale=60*30, shift=48*30)
        pil_image = Image.open(x)
        pil_image.show()
    return

    value = np.vectorize(pp.get)(t)

    plt.plot(t, value)
    plt.title(harmonics)
    plt.ylabel('%%')
    plt.xlabel('Time(t)')
    plt.show()

if __name__ == "__main__":
    __example()
