# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 19:25:44 2020

@author: Davy
"""

import time
import argparse
import cclib
import regex as re
import pandas as pd
import numpy as np
import sys
import os

def run(files, patExt):
    try:
        ext_pattern = re.compile(r'{}'.format(patExt))
    except:
        print('invalid regex pattern for file extension')
        exit(1)

    fs = []
    for i in files:
        if os.path.isfile(i):
            fs.append(i)
        else:
            for (dirpath, dirnames, filenames) in os.walk(i):
                fs.extend(['{}/{}'.format(dirpath.strip("/"), j) for j in list(filter(ext_pattern.search, filenames))])
                break

    if not fs:
        print('no valid file matches found')
        exit(1)

    df = pd.DataFrame(columns=[
                            "SPE", 
                            "HOMO_energy", 
                            "HOMO1_energy", 
                            "HOMO2_energy", 
                            "LUMO_energy", 
                            "LUMO1_energy", 
                            "LUMO2_energy",
                            "dipole", 
                            "quadrupole_XX", 
                            "quadrupole_YY", 
                            "quadrupole_ZZ", 
                            "quadrupole_XY", 
                            "quadrupole_XZ", 
                            "quadrupole_YZ", 
                            "isoquad", 
                            "hardness", 
                            "electronegativity", 
                            "electrophilicity", 
                            "electron_donating_power", 
                            "electron_accepting_power", 
                            "net_electrophilicity"])
    for ff in fs:
        data = cclib.io.ccread(ff)

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

        patSPE = "(?<=FINAL SINGLE POINT ENERGY.+)[+-]?\d+\.?\d+"
        patMag = "(?<=Magnitude.+)[+-]?\d+\.?\d+"
        patIsoQuad = "(?<=Isotropic quadrupole.+)[+-]?\d+\.?\d+"
        patQuad = "(?<=TOT.+)([+-]?\d+\.?\d+)(?=.+\(a\.u\.\))"

        SPE = []
        MAG = []
        ISO = []
        QUA = []
        with open(ff, 'r') as f:
            for l in f:
                spe = re.search(r'{}'.format(patSPE), l)
                mag = re.search(r'{}'.format(patMag), l)
                iso = re.search(r'{}'.format(patIsoQuad), l)
                qua = re.findall(r'{}'.format(patQuad), l)

                if spe is not None:
                    SPE.append(float(spe.group()))
                if mag is not None:
                    MAG.append(float(mag.group()))
                if iso is not None:
                    ISO.append(float(iso.group()))
                if qua:
                    QUA.append([float(i) for i in qua])

        float_SPE = SPE[-1]
        float_dipole = MAG[-1]
        float_isoquad = ISO[-1]
        float_quadrupole= QUA[-1]

        df = df.append({
            "SPE": SPE[-1],
            "HOMO_energy": HOMO_energy,
            "HOMO1_energy": HOMO1_energy,
            "HOMO2_energy": HOMO2_energy,
            "LUMO_energy": LUMO_energy,
            "LUMO1_energy": LUMO1_energy,
            "LUMO2_energy": LUMO2_energy,
            "dipole": MAG[-1],
            "quadrupole_XX": QUA[-1][0],
            "quadrupole_YY": QUA[-1][1],
            "quadrupole_ZZ": QUA[-1][2],
            "quadrupole_XY": QUA[-1][3],
            "quadrupole_XZ": QUA[-1][4],
            "quadrupole_YZ": QUA[-1][5],
            "isoquad": ISO[-1],
            "hardness": hardness, 
            "electronegativity": electronegativity,
            "electrophilicity": electrophilicity,
            "electron_donating_power": electron_donating_power,
            "electron_accepting_power": electron_accepting_power,
            "net_electrophilicity": net_electrophilicity
            }, ignore_index=True)

    return df

if __name__ == "__main__":
    n = str(int(time.time()))
    ofn = 'darude-{}.csv'.format(n)
    parser = argparse.ArgumentParser(prog='darude')
    parser.add_argument('-p', nargs='?', default='(?<!(_atom\d+?))\.out$', const='(?<!(_atom\d+?))\.out$', help='regex pattern for desired file extension')
    parser.add_argument('-o', nargs='?', default=ofn, const=ofn, help='specify the output filename default is \'%(prog)s.csv\'')
    parser.add_argument('file', nargs='+', help='file(s) or directories for %(prog)s to process')
    args = vars(parser.parse_args())
    ddf = run(args['file'], args['p'])
    ddf.to_csv('{}'.format(args['o']), index=False)

