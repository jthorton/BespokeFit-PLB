# BespokeFit-PLB

A real world test of [OpenFF-BespokeFit](https://github.com/openforcefield/openff-bespokefit) on the 
[Protein-Ligand Benchmark](https://github.com/openforcefield/protein-ligand-benchmark) dataset using [OpenFE protocols](https://github.com/OpenFreeEnergy/openfe). 

The goal is to evaluate the accuracy of `openff-2.2.1.offxml` with bespoke torsion parameters fit to reproduce the 
potential energy surface predicted by `aimnet2/wb97m-d3` which should offer a good balance between fitting speed and accuracy.
This repo contains the inputs and scripts used to set up and execute the calculations via [ASAP-Alchemy](https://github.com/asapdiscovery/asapdiscovery)
which has an interface to `BespokeFit`. All calculations were executed on [Alchemiscale](https://github.com/OpenFreeEnergy/alchemiscale).


