# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 11:17:56 2023

@author: szoti
"""

import os

import matplotlib.pyplot as plt
import core
import util



def find_nucids(mass_file_name : str) -> list:
    
    mass_file = open(mass_file_name, "r")
    lines = mass_file.readlines()
    nucid_list = []
    for l in lines:
        l_start = l[0:5]
        nuc_id = l_start.strip()
        if len(nuc_id) >=3 and not nuc_id.isnumeric() and\
            nuc_id not in nucid_list:
                nucid_list.append(nuc_id)

    mass_file.close()
    return(nucid_list)


def nucid_list_2_nuclide_list(nucid_list : list) -> list:
    
    nuclide_list = []
    for nucid in nucid_list:
        nuclide_list.append(util.az_from_nucid(nucid))
    return(nuclide_list)


def collect_isomer(iso, i):
    
    ip = {}
    
    if i == 0:
        ip["iso"] = False
    else:
        ip["iso"] = True
    ip["decay_id"] = iso.prop["T"].split()[:2]   
    ip["Jp"] = iso.prop["J"]
    ip["E-level"] = iso.prop["E"] + "keV"
    ip["Half-life"] = iso.half_life
    ip["Decay_modes"] = {}
    for dm in iso.decay_ratio:
        ip["Decay_modes"][dm] = {"ratio" : iso.decay_ratio[dm]}
    return(ip)

def add_b_minus_alpha_IT_q_values(isomer_list, nuc):
    for isop in isomer_list:
        for idecm in isop["Decay_modes"]:
            if idecm == "B-":
                isop["Decay_modes"][idecm]["Q-value"] =\
                    nuc.adopted_levels.qrecords[0].q_beta_minus
            if idecm == "A":
                isop["Decay_modes"][idecm]["Q-value"] =\
                    nuc.adopted_levels.qrecords[0].alpha_decay
            if idecm == "IT":
                isop["Decay_modes"][idecm]["Q-value"] =\
                    isop["E-level"]  

def add_emissions(isomer_list, nuc):
    pass
    
    
    
    
# main part
ensdf = core.get_active_ensdf()

mass_file_name = "ensdf.190"
mass_file_name = os.getcwd() + "/../ensdf_full/" + mass_file_name
nucid_list = find_nucids(mass_file_name)
nuclide_list = nucid_list_2_nuclide_list(nucid_list)

for tup in nuclide_list:
    print("new nuclide")
    print("tup", tup)
    nuc = core.Nuclide(tup[0], tup[1])
    isomers = nuc.get_isomers()
    isomers_to_print = []
    i = 0
    for iso in isomers:
        if i == 0 :
             isomers_to_print.append(collect_isomer(iso, i))
           #print(iso.decays)
        elif i > 0 :
            if len(iso.decay_ratio) == 1:
                if "IT" in iso.decay_ratio:
                    
                    if "PS" in iso.prop["T"] or "NS" in iso.prop["T"] or\
                        "US" in iso.prop["T"] or "MS" in iso.prop["T"]:
                            continue
                    elif " S" in iso.prop["T"] and iso.half_life < 1.0:
                        continue
                    else:                        
                        isomers_to_print.append(collect_isomer(iso, i))
                else:                   
                    isomers_to_print.append(collect_isomer(iso, i))
            else:
                isomers_to_print.append(collect_isomer(iso, i))
            #print(iso.decays)

        i += 1
        if i > 2:
            break
    
    add_b_minus_alpha_IT_q_values(isomers_to_print, nuc)
    add_emissions(isomers_to_print, nuc)
                                                
    print(isomers_to_print)
    print(nuc.adopted_levels.qrecords)
    