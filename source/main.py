# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 14:41:51 2023

@author: szoti
"""
import matplotlib.pyplot as plt
import core
import inspect



def level_scheme(nuc=None, nucleons=None, protons=None):
    decays = []
    if not nuc:
        nuc = core.Nuclide(nucleons, protons)
    print(nuc)
    for level in nuc.adopted_levels.levels:
        print("level", level)
        print(level.decays)
        decays.extend(level.decays)
        # print(level)
    
    i = 0.5
    for level in nuc.adopted_levels.levels:
#        print(level)
        plt.axhline(level.energy.val, color='k')
        for decay in level.decays:
 #           print(decay)
            plt.plot(
                [i, i],
                [decay.orig_level.energy.val, decay.dest_level.energy.val]
            )
            i += 1
    print("decay",decay)
    plt.xlim(0, i - 0.5)
    plt.ylim(0, nuc.adopted_levels.levels[-1].energy.val)
    plt.show()

def list_levels(nuc=None, nucleons=None, protons=None):
    if not nuc:
        nuc = core.Nuclide(nucleons, protons)
    for l in nuc.adopted_levels.levels:
        hl = str(l.half_life)
        if hl[0] not in "<>≤≥":
            hl = f"= {hl}"
#        print(f"E = {l.energy}. Jπ = {l.ang_mom}. λ {hl}.")  

def bra_unc(value):
    if len(value.split())> 1:
        val_bra = value.split()[0] + " (" + value.split()[1] +")"
        return(val_bra)
    else:
        return(value)

def out_wiki(n, cat, adopt):
    of = "../out_wiki"
    if n["iso"] == 0:
        nt = open(of+"/"+n["name"], "w", encoding="utf-8")
    elif n["iso"] == 1:
        nt = open(of+"/"+n["name"] +"m", "w", encoding="utf-8")
    elif n["iso"] == 2:
        nt = open(of+"/"+n["name"] +"n", "w", encoding="utf-8")
    print(cat, file = nt)
    print(file = nt)
    print(adopt, file = nt)
    print(file = nt)
#    print(str(latex(pi))
    print("Jπ:", file = nt)
    if n["Jp"].isspace():
        print(" ?", file = nt)
    else:
        print( n["Jp"], file = nt)
    if not n["E-level"].isspace():
        print("  E-level: " +  n["E-level"], file = nt)
    print(file = nt)
    print("Half-life:", file = nt)
    if n["Half-life"]:
        st = str(n["Half-life"]).replace("min", "m")
        st = st.replace("hour", "h")
        st = st.replace("year", "a")        
        print("",st, file = nt)
    
    if len(n["Decay_modes"]) > 0:
        print(file = nt)
        print("Decay modes:", file = nt)
        for dm in n["Decay_modes"]:
            if dm == "B-":
                nt.write(" ß- = " + str(n["Decay_modes"][dm]["ratio"]))
                ql = n["Decay_modes"][dm]["Q-value"].split()
                if len(ql) > 1:
                    stq = ql[0] + " (" + ql[1] + ") keV"
                nt.write("          Q = " + stq + "\n")
            
           
            max_prob = 0
            max_energ = 0
            for de in n["Decay_modes"][dm]["Emissions"]:
                prob = float(n["Decay_modes"][dm]["Emissions"][de]["Prob"].split()[0])
                if prob > max_prob:
                    max_prob = prob
                    pr_max_prob = n["Decay_modes"][dm]["Emissions"][de]["Prob"]
                    energ_max_prob = n["Decay_modes"][dm]["Emissions"][de]["Energy"]
                    dest_lev_max_prob = n["Decay_modes"][dm]["Emissions"][de]["Dest_level"]
                energ = float(n["Decay_modes"][dm]["Emissions"][de]["Energy"].split()[0])
                if energ > max_prob:
                    max_energ = energ
                    pr_max_energ = n["Decay_modes"][dm]["Emissions"][de]["Energy"]
                    prob_max_energ = n["Decay_modes"][dm]["Emissions"][de]["Prob"]
                    dest_lev_max_energ = n["Decay_modes"][dm]["Emissions"][de]["Dest_level"]
                    
            print(pr_max_prob, energ_max_prob, dest_lev_max_prob)
            print(prob_max_energ, pr_max_energ, dest_lev_max_energ)
            
            if len(n["Decay_modes"][dm]["Emissions"]) > 0: 
                print(file=nt)               
                print("Radiations:", file=nt)
                dot3 = False
                if dm == "B-":
                    nt.write(" ß- -decay (" + str(n["Decay_modes"][dm]["ratio"]) +")\n")
                    nt.write(" β- emissions:\n")
                    nt.write(" Eβ(MeV)       E(level)(keV)  Rel.Iβ        Comments \n")
                    nt.write(" -------------------------------------------------------\n") 
                    #print(bra_unc(energ_max_prob))
                    nt.write(" " + bra_unc(energ_max_prob) + "      " + bra_unc(dest_lev_max_prob)\
                             + "     " + bra_unc(pr_max_prob) + "\n")
                    if len(n["Decay_modes"][dm]["Emissions"]) > 1:
                        if float(dest_lev_max_prob.split()[0]) != float(dest_lev_max_energ.split()[0]):
                            nt.write(" " + bra_unc(pr_max_energ) + "      " + bra_unc(dest_lev_max_energ)\
                                     + "     " + bra_unc(prob_max_energ) + "\n")
                        else:
                            dot3 = True
                            nt.write(" ...\n")
                    if len(n["Decay_modes"][dm]["Emissions"]) > 2 and not dot3:
                        nt.write(" ...\n")
                    nt.write(" -------------------------------------------------------\n")
                    print("beta norm", n["Decay_modes"][dm]["Beta_norm"] + "...")
                    if n["Decay_modes"][dm]["Beta_norm"].strip() == "1":
                        print("beta norm", n["Decay_modes"][dm]["Beta_norm"])
                        outs = n["Decay_modes"][dm]["Beta_norm"].strip() + ".00"
                        nt.write(" For abs. intensity per 100 decays, multiply by "+ outs + ".\n")
                    else:
                        nt.write("For abs. intensity per 100 decays, multiply by " + n["Decay_modes"][dm]["Beta_norm"] +".\n")
                    gamma_norm = n["Decay_modes"][dm]["Gamma_norm"]
            if len(n["Gammas"]) > 0:
                ind = 1
                print(file=nt)
                print(" γ radiation:", file = nt)
                print("  Eγ(keV)       E(level)      Rel.Iγ        α(tot)        Comments", file=nt)      
                print(" ---------------------------------------------------------------------", file=nt)
                
                for g in n["Gammas"]:
                    nt.write(" " + bra_unc(g[1]) + "     " + g[2] + "          " + bra_unc(g[3]))
                    nt.write("       " + bra_unc(g[4]))
                    if not g[4].isspace() :
                        if float(g[4].split()[0] ) >=1 :
                            nt.write("     " + "e-")
                    nt.write("\n")
                    ind += 1
                    if ind > 5:
                        break
                
                if len(n["Gammas"]) >5:
                    print(" ...", file=nt)    
                nt.write(" --------------------------------------------------------------------\n")
                nt.write(" For abs. intensity per 100 decay, multiply by " + 
                                 bra_unc(gamma_norm)+ ".\n")
                        
                            
                    
                    # if len(n["Decay_modes"][dm]["Gammas"]) > 0:
                    #     print("gammas")
                                 
                    
                            
                    
                    
             
            
    print(n["name"])
    nt.close()
        
ensdf = core.get_active_ensdf()
#print(ensdf)


#for ds in ensdf.datasets:
#    print(ds)
#ds1 = ensdf.get_dataset((190, 74), '190TA B- DECAY (5.3 S)')
#al1 = ensdf.get_adopted_levels((190,74))
#in1 = ensdf.get_indexed_nuclides()
#level_scheme(nucleons=190, protons=77)
#list_levels(nucleons=190, protons=77)
#a = ensdf.get_datasets_by_nuclide((190, 74))
nuc = core.Nuclide(190, 72)
#print(nuc.adopted_levels)
#for ds in nuc.adopted_levels:
#    print(ds.dataset_id)
#print(nuc.adopted_levels.dataset_id)
#print(nuc.adopted_levels.jpi_index)
#print(nuc.adopted_levels.header)
#print(nuc.adopted_levels.nucid)
# print(nuc.adopted_levels.dataset_ref)
# print(nuc.adopted_levels.publication)
# print(nuc.adopted_levels.date)
#print(nuc.adopted_levels.records)
#print(nuc.adopted_levels.levels)
for l in nuc.adopted_levels.levels:
    print("propl",l.prop["L"])
    for key in l.prop:
        print(key, l.prop[key])
        
#print(nuc.adopted_levels.history)
#print("qrecords",nuc.adopted_levels.qrecords)
#print(nuc.adopted_levels.normalization_records)
#print(nuc.adopted_levels.parents)
#print(nuc.adopted_levels.references)

l0 = {"name" : str(nuc)}


nuciso = nuc.get_isomers()
# for iso in nuciso:
#     print(iso)
#    print(iso.prop["T"])
#    print(iso.populating)
#    print(iso.decays)
#    print(core.get_record_type(iso))
daugh = nuc.get_daughters()
i = 0
#for da in daugh:
#     print(da)
     # if i == 1:
     #     ds = ensdf.get_dataset(da[0], da[1])
     #     for key in ds.records:
     #         if type(key).__name__ == "BetaRecord":
     #             print(key.dest_level)
     #             print(key.prop["E"])
     #             print(key.prop["IB"])
     #             print(key.prop["Q"])
# #                 print(key.dataset)
# #         print(ds.dataset_id)
#          print(ds.records)
#     i += 1
# print(l0["name"])
#level_scheme(nuc=None, nucleons=190, protons=75)
print("New nuclide\n", i)
print("q-val",nuc.adopted_levels.qrecords[0].prop["Q-"])
# print("nuc", nuc)
# print("nuciso", nuciso)
nuciso = nuc.get_isomers()

i=0
# print("i, l", i)
for l in nuciso:

     if i == 0:
         l0["iso"] = False
         l0["Jp"] = l.prop["J"]
         l0["E-level"] = l.prop["E"] + "keV"
         l0_id = l.prop["T"].split()[:2]
         l0["Half-life"] = l.half_life
#         print("qv",l.prop["Q"])
         l0["Decay_modes"] = {}
#         print(l.decay_ratio)
         for k in l.decay_ratio:
#             print(k)
             l0["Decay_modes"][k] = {"ratio" : l.decay_ratio[k]}
#             print(l0["Decay_modes"])
#             print(l0["Half-life"])
#             print(l0_id)
             has_daugh = False
             for d in nuc.get_daughters():
                 has_daugh = True
                 if k in d[1] and l0_id[0] in d[1] and l0_id[1] in d[1]:
                     #print("daugh", d)
                     dec_dat = ensdf.get_dataset(d[0], d[1])
                     print("getdata end")
                     l0["Decay_modes"][k]["ref"] = dec_dat.history["CIT"]
                     l0["Decay_modes"][k]["cutoff"] = dec_dat.history["CUT"]
                     l0["Decay_modes"][k]["Beta_norm"] = dec_dat.normalization_records[0].prop["NB"]
                     l0["Decay_modes"][k]["Gamma_norm"] = dec_dat.normalization_records[0].prop["NR"]
                    # print(l0["Decay_modes"][k]["Beta_norm"])
#                     print("qrec",dec_dat.records)
#                     print(k)
                     #print("norm rec",dec_dat.normalization_records[0].prop["NB"])
                     em = 0
                     if k == "B-":
                         l0["Decay_modes"][k]["Emissions"] = dict()
                         for rec in dec_dat.records:
#                             print(rec)

                             if type(rec).__name__ == "BetaRecord":
#                                 print("dest level", rec.dest_level)
                                 em += 1
#                                 print("em", em)
                                 #print(nuc.adopted_levels.qrecords[0].prop["Q-"])
                                 l0["Decay_modes"][k]["Q-value"] = nuc.adopted_levels.qrecords[0].prop["Q-"]
                                
                                 l0["Decay_modes"][k]["Emissions"][em] = dict()
                                 if rec.prop["E"].isspace():
#                                     print("no energy")
                                     Qs = l0["Decay_modes"][k]["Q-value"].split()
                                     Qv = float(Qs[0])
                                     dls = rec.dest_level.prop["E"].split()
                                     Ev = float(dls[0])
#                                     print(dls)
                                     Enp_en= str(round(Qv - Ev))
#                                     print(Enp_en)
                                     l0["Decay_modes"][k]["Emissions"][em]["Energy"] = Enp_en + " " + Qs[1]
                                 else:
                                     l0["Decay_modes"][k]["Emissions"][em]["Energy"] = rec.prop["E"]
#                                     print(rec.prop["E"])
                                 l0["Decay_modes"][k]["Emissions"][em]["Prob"] = rec.prop["IB"]
#                                 print(rec.prop["IB"])
                                 l0["Decay_modes"][k]["Emissions"][em]["Dest_level"] = rec.dest_level.prop["E"]
#                                 print(l0["Decay_modes"][k]["Emissions"][em]["Prob"])
                    
                     dec_dat = ensdf.get_dataset(d[0], d[1])
#                     print(len(dec_dat.records))
                     ii = 0
                     collect = False
                     #0["Gammas"] = []
                     gamma_l = []
                     for rec in dec_dat.records:
                         if type(rec).__name__ == "GammaRecord":
                            # print(rec)
                             #print( rec.energy)
                             #print(rec.dest_level.energy)
                             g_level = str(round(rec.energy.val + rec.dest_level.energy.val, 2))
                             g_energ = rec.prop["E"]
                             g_intens = rec.prop["RI"]
                             g_conv = rec.prop["CC"]
                             #print(g_intens)
                             rel_g_intens = rec.rel_intensity
                             gamma_l.append([rel_g_intens, g_energ, g_level, g_intens, g_conv])
                             #print(rel_g_intens, g_energ, g_level, g_intens, g_conv)
                     l0["Gammas"] = sorted(gamma_l, key=lambda x: x[0], reverse=True)
             if not has_daugh:
                 if k == "B-":
                     l0["Decay_modes"][k]["Q-value"] = nuc.adopted_levels.qrecords[0].prop["Q-"]
                 continue  
              
     i += 1
#print(nuciso)
#print(in1)
#print(ds1)

cat = "[[Category:NuclideInfo.Nuclides2023]]"
adopt = "=== Adopted values 12th edition ==="

out_wiki(l0, cat, adopt)


