# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 19:25:44 2020

@author: Davy
"""

import cclib
import re
import pandas as pd
import numpy as np

filename = "agonist1_orca_output.out"

data = cclib.io.ccread(filename)
print("There are %i atoms and %i MOs" % (data.natom, data.nmo))

HOMO_energy = data.moenergies[0][data.homos[0]]*0.036749305
HOMO1_energy = data.moenergies[0][data.homos[0]-1]*0.036749305
HOMO2_energy = data.moenergies[0][data.homos[0]-2]*0.036749305

LUMO_energy = data.moenergies[0][data.homos[0]+1]*0.036749305
LUMO1_energy = data.moenergies[0][data.homos[0]+2]*0.036749305
LUMO2_energy = data.moenergies[0][data.homos[0]+3]*0.036749305

hardness = LUMO_energy - HOMO_energy

electronegativity = (HOMO_energy+LUMO_energy)/2

electrophilicity = ((HOMO_energy+LUMO_energy)**2)/((LUMO_energy-HOMO_energy)*4)

electron_donating_power = (3*(HOMO_energy)+(LUMO_energy))**2/(16*(hardness))

electron_accepting_power = ((HOMO_energy)+(3*(LUMO_energy)))**2/(16*(hardness))

net_electrophilicity = electron_donating_power + electron_accepting_power

SPE_pattern = "FINAL SINGLE POINT ENERGY"
file = open(filename, "r")
for line in file:
    if re.search(SPE_pattern, line):
        found_SPE = line        
formatted_SPE = re.findall(r"[-+]?\d*\.\d+|\d+",found_SPE)
float_SPE = [float(item) for item in formatted_SPE]
print(float_SPE)

dipole_pattern = "Magnitude"
file = open(filename, "r")
for line2 in file:
    if re.search(dipole_pattern, line2):
        found_dipole = line2        
formatted_dipole = re.findall(r"[-+]?\d*\.\d+|\d+",found_dipole)
float_dipole = [float(item) for item in formatted_dipole]
print(float_dipole)

isoquad_pattern = "Isotropic quadrupole"
file = open(filename, "r")
for line3 in file:
    if re.search(isoquad_pattern, line3):
        found_isoquad = line3        
formatted_isoquad = re.findall(r"[-+]?\d*\.\d+|\d+",found_isoquad)
float_isoquad = [float(item) for item in formatted_isoquad]
print(float_isoquad)

rawquadrupole_pattern = 'TOT       '
file = open(filename, "r")
for line4 in file:
    if re.findall(rawquadrupole_pattern, line4):
        found_rawquadrupole = line4        
formatted_quadrupole =re.findall(r"[-+]?\d*\.\d+|\d+",found_rawquadrupole)
float_quadrupole = [float(item) for item in formatted_quadrupole]
print(float_quadrupole)

#quadrupole order: XX YY ZZ XY XZ YZ


SPE = np.asarray(float_SPE)
dipole = np.asarray(float_dipole)
isoquad = np.asarray(float_isoquad)
quadrupole = np.asarray(float_quadrupole)

np_catlist = np.concatenate((SPE,HOMO_energy, HOMO1_energy, HOMO2_energy, LUMO_energy, LUMO1_energy, LUMO2_energy,dipole, quadrupole, isoquad, hardness, electronegativity, electrophilicity, electron_donating_power, electron_accepting_power, net_electrophilicity),axis=None)

df = pd.DataFrame(np_catlist.reshape(-1, len(np_catlist)),columns=["SPE","HOMO_energy", "HOMO1_energy", "HOMO2_energy", "LUMO_energy", "LUMO1_energy", "LUMO2_energy","dipole", "quadrupole_XX", "quadrupole_YY", "quadrupole_ZZ", "quadrupole_XY", "quadrupole_XZ", \
                  "quadrupole_YZ", "isoquad", "hardness", "electronegativity", "electrophilicity", "electron_donating_power", "electron_accepting_power", "net_electrophilicity"])
print(df)

df.to_csv(r'DaRuDE_v0_Output.csv', index=False)