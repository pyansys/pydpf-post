"""
.. _ref_mesh_external_layer_compare_example:

Validate external layer results with the full mesh
==================================================
This example shows postprocessing comparisons based on how results and
the mesh are extracted:

- Results and mesh extracted only on the external layer
- Results and mesh extracted on the entire mesh

The external layer is the layer of solid elements with at least one facet facing the outside of
the geometry.

This feature, available for all types of mechanical simulation, allows you to reduce the size
of both the mesh and extracted data to improve processing performance.
Because larger stresses and strains are usually located on the skin of a model,
computing the results on the external layer provides equivalent maximum values in most cases.
"""

###############################################################################
# Perform required imports
# ------------------------
# Perform required imports. This example uses a supplied file that you can
# get using the ``examples`` module.

from ansys.dpf import post
from ansys.dpf.post import examples

###############################################################################
# Get ``Simulation`` object
# -------------------------
# Get the ``Simulation`` object that allows access to the result. The ``Simulation``
# object must be instantiated with the path for the result file. For example,
# ``"C:/Users/user/my_result.rst"`` on Windows or ``"/home/user/my_result.rst"``
# on Linux.

example_path = examples.download_crankshaft()
# to automatically detect the simulation type, use:
simulation = post.load_simulation(example_path)

# to enable auto-completion, use the equivalent:
simulation = post.StaticMechanicalSimulation(example_path)

# print the simulation to get an overview of what's available
print(simulation)

###############################################################################
# Extract displacement data
# -------------------------
# Extract displacement data over the entire mesh and on the external layer.

displacement_ext = simulation.displacement(external_layer=True)
displacement = simulation.displacement()  # default is external_layer=False
displacement_ext.plot()
displacement.plot()

print(
    f"number of nodes with external_layer=True: {len(displacement_ext.index.mesh_index)}"
)
print(
    f"number of nodes with external_layer=False: {len(displacement.index.mesh_index)}"
)

###############################################################################
# Extract stress and strain data
# -------------------------------
# Extract stress and elastic strain data over the entire mesh and on the external layer.
# You can easily compute averages and invariants on the external layer because the
# connectivity of the kept elements remains unchanged.

elemental_stress_ext = simulation.stress_principal_elemental(
    components=[1], external_layer=True
)
elemental_stress = simulation.stress_principal_elemental()
elemental_stress_ext.plot()
elemental_stress.plot()

print(
    f"number of elements with external_layer=True: {len(elemental_stress_ext.index.mesh_index)}"
)
print(
    f"number of elements with external_layer=False: {len(elemental_stress.index.mesh_index)}"
)

elastic_strain_eqv_ext = simulation.elastic_strain_eqv_von_mises_nodal(
    external_layer=True
)
elastic_strain_eqv = simulation.elastic_strain_eqv_von_mises_nodal()
elastic_strain_eqv_ext.plot()
elastic_strain_eqv.plot()
