# loop over the networks and make sure we find some bespoke parameters and print the stats on covered ligands
import pathlib
import pandas as pd
from asapdiscovery.alchemy.schema.fec import FreeEnergyCalculationNetwork
from openff.toolkit import Molecule

bespoke_data = []
bespoke_dir = pathlib.Path("../bespokefit_benchmarks")
for network_file in bespoke_dir.glob("**/planned_network.json"):
    network = FreeEnergyCalculationNetwork.from_file(network_file.as_posix())
    name = network.dataset_name
    for ligand in network.network.ligands:
        bespoke_data.append({
            "Network": name, 
            "Ligand_name": ligand.compound_name, 
            "BespokeFit_ID": ligand.tags["bespokefit_id"], 
            "Smiles": ligand.provenance.isomeric_smiles, 
            "BespokeParameters": True if ligand.bespoke_parameters is not None else False
            })
        # make sure that each of the bespoke parameters can be applied to the molecule
        off_mol: Molecule = Molecule.from_smiles(ligand.provenance.isomeric_smiles)
        if ligand.bespoke_parameters is not None:
            for parameter in ligand.bespoke_parameters.parameters:
                # make sure we have some matches
                assert bool(off_mol.chemical_environment_matches(parameter.smirks)) is True
df = pd.DataFrame(bespoke_data)
print(df)
df.to_csv("bespokefit_parameter_mapping.csv")
