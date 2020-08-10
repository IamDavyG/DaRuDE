# DaRuDE
Davy's Rudimentary Descriptor Extractor (DaRuDE) is a Python script that extracts 21 quantum mechanical descriptors that are output by the MaPhi descriptor program from Orca output files.

## What DaRuDE does
1. Extract 21 descriptors from Orca output files into a .csv retaining the same order as MaPhi

## What DaRuDE doesn't do
1. Generate initial geometries or input files
2. Optimise geometries
3. Check geometry optimisation convergence
4. Visualise molecular orbitals
5. Extract descriptors for more than one Orca output file

## Orca Input Prerequisites
Orca input files must contain the following code block to calculate the raw data that DaRuDE extracts
```
%output
	print[P_MOs] true
end
%elprop
    Quadrupole True
end
```

## Dependencies
### install requirements
`pip install -r requirements.txt`
* cclib
* regex
* pandas
* numpy

## To do
- Make an install script for a Conda environment

