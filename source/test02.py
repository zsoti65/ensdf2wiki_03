# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:39:42 2023

@author: szoti
"""

import os

import matplotlib.pyplot as plt
import core
import util

ensdf = core.get_active_ensdf()
nuc = core.Nuclide(190, 73)
iso = nuc.get_isomers()
for l in iso:
    print(l.prop["T"])
    print(l.decay_ratio)
    for p in l.prop:
        print(p, l.prop[p])