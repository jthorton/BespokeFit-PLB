from openff.qcsubmit.common_structures import QCSpec
from openff.bespokefit.workflows import BespokeWorkflowFactory


# create the AIMNET2 spec
aimnet2 = QCSpec(
    method="wb97m-d3",
    basis=None,
    program="aimnet2",
    spec_description="ASAP-Alchemy standard aimnet2 protocol"
)

factory = BespokeWorkflowFactory(default_qc_specs=[aimnet2], initial_force_field="openff_unconstrained-2.2.1-rc1.offxml")
# up the iterations for large molecules! 
factory.optimizer.max_iterations = 20

factory.to_file("aimnet2-bespoke-factory.json")
