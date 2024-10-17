# loop over the networks and make sure we find some bespoke parameters and print the stats on covered ligands
import pathlib
import pandas as pd
from asapdiscovery.alchemy.schema.fec import FreeEnergyCalculationNetwork

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
df = pd.DataFrame(bespoke_data)
print(df)
df.to_csv("bespokefit_parameter_mapping.csv")
