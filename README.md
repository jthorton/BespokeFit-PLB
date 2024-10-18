# BespokeFit-PLB

A real world test of [OpenFF-BespokeFit](https://github.com/openforcefield/openff-bespokefit) on the 
[Protein-Ligand Benchmark](https://github.com/openforcefield/protein-ligand-benchmark) dataset using [OpenFE protocols](https://github.com/OpenFreeEnergy/openfe). 

The goal is to evaluate the accuracy of `openff-2.2.1.offxml` with bespoke torsion parameters fit to reproduce the 
potential energy surface predicted by `aimnet2/wb97m-d3` which should offer a good balance between fitting speed and accuracy.
This repo contains the inputs and scripts used to set up and execute the calculations via [ASAP-Alchemy](https://github.com/asapdiscovery/asapdiscovery)
which has an interface to `BespokeFit`. All calculations were executed on [Alchemiscale](https://github.com/OpenFreeEnergy/alchemiscale).


## Input Generation

All of the inputs were prepared using the `ASAP-Alchemy` CLI following the steps listed, before starting you will need 
to download a copy of the `Protein Ligand Benchmark (PLB)` curated by OpenFE from [zenodo](https://zenodo.org/records/13165855).
This benchmark dataset contains a series of Minimal Spanning Tree (MST) OpenFE `LigandNetworks` generated using the 
[Kartograf atom mapper](https://github.com/OpenFreeEnergy/kartograf), [Lomap transformation](https://github.com/OpenFreeEnergy/Lomap)
scorer with OpenEye `AM1BCCELF10` partial charges. You will then need to download the `receptor PDB files` found on the 
[PLB repo](https://github.com/OpenFreeEnergy/protein-ligand-benchmark/tree/main/data).


### Creating the `FreeEnergyCalculationNetwork`

 First we need to define the runtime settings we want to use in the OpenFE protocol, this can be done using the 
 `create_alchemy_settings.py` script which will produce two relative binding free energy protocol settings files. The 
 first `alchemy_factory_openff_2_2_1.json` is the settings file for `ASAP-Alchemy` which we will reuse the second, 
 `openfe_protocol_settings.json` is the OpenFE equivalent file provided for provenance.
 
Then for each of the networks we want to benchmark we can generate the `FreeEnergyCalculationNetwork` using the CLI and 
our settings file:

```shell
asap-alchemy plan --factory-file "alchemy_factory_openff_2_2_1.json"    \
                  --name "tyk2_default"                                 \
                  --receptor "receptors/tyk2.pdb"                       \
                  --graphml "tyk2.graphml"
```

This example will produce a `FreeEnergyCalculationNetwork` for the `TYK2` system.


### BespokeFit

`ASAP-Alchemy` has an interface to `OpenFF-Bespokefit` to streamline the generation of bespoke torsion parameters for 
a `FreeEnergyCalculationNetwork`. In this example we will be using a custom BespokeFit protocol which uses the AIMNET2 
ML model as the reference potential. The BespokeFit workflow can be generated using the `create_bespoke_workflow.py` 
script, this will produce a settings file called `aimnet2-bespoke-factory.json`.

Then for each of our planned networks we can use the `ASAP-Alchemy` CLI to submit the BespokeFit jobs via:

```shell
asap-alchemy bespoke submit --network "tyk2_bespoke/planned_network.json"     \
                            --factory-file "aimnet2-bespoke-factory.json"
```

Each ligand will have a BespokeFit task id generated and saved into the input network which is later used to check the 
status of the task and to gather the results.

The status of the parameterization job can be checked using:

```shell
asap-alchemy bespoke status --network "tyk2_bespoke/planned_network.json"
```

Once all the optimisations have finished the results can be gathered and stored into the `planned_netwrok.json` via:

```shell
asap-alchemy bespoke gather --network "tyk2_bespoke/planned_network.json"
```

in some cases you might some molecules can not be parameterised, to skip these missing results use:

```shell
asap-alchemy bespoke gather --network "tyk2_bespoke/planned_network.json"   \
                            --allow-missing
```

## Submission

Each of the bespoke and default networks can then be submitted to `Alcehmiscale` via:

```shell
asap-alchemy submit --network "tyk2_bespoke/planned_network.json"    \
                     --organization "openfe"                         \
                     --campaign "public"                             \
                     --project "benchmark_tyk2_bespoke"              \
                     --repeats 3  
```

This will generate a network key and store it into the input network file which can be used to quickly lookup the 
network in future when checking its status or gathering the results.


## Results

Once the network of simulations has completed we can gather the results via:

```shell
asap-alchemy gather --network "tyk2_bespoke/planned_network.json"
```