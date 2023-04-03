"""
.. _ref_cyclic_results_example:

Extract cyclic results
======================
In this script a modal analysis with cyclic symmetry is processed to show
how to expand the mesh and results.
"""

###############################################################################
# Perform required imports
# ------------------------
# Perform required imports. # This example uses a supplied file that you can
# get by importing the DPF ``examples`` package.

from ansys.dpf import post
from ansys.dpf.post import examples

###############################################################################
# Get ``Simulation`` object
# -------------------------
# Get the ``Simulation`` object that allows access to the result. The ``Simulation``
# object must be instantiated with the path for the result file. For example,
# ``"C:/Users/user/my_result.rst"`` on Windows or ``"/home/user/my_result.rst"``
# on Linux.

example_path = examples.find_simple_cyclic()
simulation = post.ModalMechanicalSimulation(example_path)

# print the simulation to get an overview of what's available
print(simulation)

#############################################################################
# Extract expanded displacement norm
# ----------------------------------

displacement_norm = simulation.displacement(
    norm=True,
    expand_cyclic=True,
)
print(displacement_norm)
displacement_norm.plot()

#############################################################################
# Extract equivalent von mises nodal stress expanded on the first four sectors
# ----------------------------------------------------------------------------

stress_vm_sectors_0_1_2_3 = simulation.stress_eqv_von_mises_nodal(
    expand_cyclic=[0, 1, 2, 3],
)
print(stress_vm_sectors_0_1_2_3)
stress_vm_sectors_0_1_2_3.plot()

#############################################################################
# Extract equivalent von mises nodal stress without expansion
# -----------------------------------------------------------

stress_vm_sector_0 = simulation.stress_eqv_von_mises_nodal(
    expand_cyclic=False,
)
print(stress_vm_sector_0)
stress_vm_sector_0.plot()
