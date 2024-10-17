"Create the factory settings file which will be applied to all of the benchmarks"
from asapdiscovery.alchemy.schema.fec import FreeEnergyCalculationFactory
from openff.units import unit
import json
from gufe.tokenization import JSON_HANDLER

factory = FreeEnergyCalculationFactory()

# set the box shape
factory.solvation_settings.box_shape = "dodecahedron"
# we need to make this bigger so we don't have crashes in the solvent phase, but has too many waters in the complex phase
factory.solvation_settings.solvent_padding = 1.5 * unit.nanometer
# set the base force field to be used
factory.forcefield_settings.small_molecule_forcefield = "openff-2.2.1.offxml"
# reduce the non-bonded cutoff to the openff default
factory.forcefield_settings.nonbonded_cutoff = 0.9 * unit.nanometer

# save the factory to file to use with the CLI to create the networks
factory.to_file("alchemy_factory_openff_2_2_1.json")

# dump out the openfe protocol
openfe_protocol = factory.to_openfe_protocol()
with open("openfe_protocol_settings.json", "w") as out:
    json.dump(
        openfe_protocol.to_dict(),
        out,
        cls=JSON_HANDLER.encoder
    )


