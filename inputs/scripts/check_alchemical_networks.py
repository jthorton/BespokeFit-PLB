# check that the alchemical networks made by alchemy use the provided charges and have bespoke parmaters
import pathlib
from asapdiscovery.alchemy.schema.fec import FreeEnergyCalculationNetwork
import warnings


bespoke_dir = pathlib.Path("../bespokefit_benchmarks")
for network_file in bespoke_dir.glob("**/planned_network.json"):
    network = FreeEnergyCalculationNetwork.from_file(network_file.as_posix())
    print("Checking ", network.dataset_name)
    # make sure the charges are picked up
    with warnings.catch_warnings(record=True) as w:
        openfe_network = network.to_alchemical_network()
        assert len(w) == 1
        assert "Partial charges have been provided, these will preferentially be used instead of generating new partial charges" in str(w[0].message)
        for transform in openfe_network.edges:
            # make sure its the full offxml string
            assert transform.protocol.settings.forcefield_settings.small_molecule_forcefield != "openff-2.2.1.offxml"
            assert len(transform.protocol.settings.forcefield_settings.small_molecule_forcefield) > 1000