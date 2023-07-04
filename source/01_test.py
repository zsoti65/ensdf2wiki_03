# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 16:23:57 2023

@author: szoti
"""

import matplotlib.pyplot as plt
import core
import inspect#

ensdf = core.get_active_ensdf()

print("START")

nuc = core.Nuclide(190, 73)
print("nuc", nuc)
#for l in nuc.adopted_levels.levels:
#    print(l)
isomers = nuc.get_isomers()
print(isomers)

print(nuc.adopted_levels.qrecords)
for iso in isomers:
    print(iso)
    for key in iso.prop:
        print(key, iso.prop[key])

doughters = nuc.get_daughters()
print("Doughters", nuc)
for d in doughters:
    print("dough", d)
    dsd = ensdf.get_dataset(d[0],d[1])
    for r in dsd.levels:
        print("d levels",r)
    for rr in dsd.records:
        print("dsd recorde", rr)

# dsbn = ensdf.get_datasets_by_nuclide((190,81))
# print(nuc)
# print("dsbn", dsbn)
# for ds in dsbn:
#     print("datasets",ds)
#    print(key, isomers.prop[k])
    
# print(nuc.adopted_levels.jpi_index)
# print(nuc.adopted_levels.header)
# print(nuc.adopted_levels.date)
# print("RECORDS")
# print(nuc.adopted_levels.records)
# print("Levels")
# print(nuc.adopted_levels.levels)
# print("QREC")
# print(nuc.adopted_levels.qrecords)
# print("Normalization")
# print(nuc.adopted_levels.normalization_records)
# print("parents")
# print(nuc.adopted_levels.parents)      