"""Pseudocode for PyDPF-Post Harmonic Mechanical Simulations APIs."""

import ansys.dpf.post as dpf
from ansys.dpf.post import examples
from ansys.dpf.post.selection import Selection

# Provide Enums for available physics_types and analysis_types
# from ansys.dpf.post import physics_types, analysis_types


harmonic_simulation = dpf.load_simulation(examples.complex_rst)
# harmonic_simulation = dpf.load_simulation(examples.complex_rst,
#                                           physics_type=physics_types.mechanical,
#                                           analysis_type=analysis_types.harmonic)

# -----------------------------------------------------------------------------------------
# Explore the simulation metadata

# Print information about the simulation
print(harmonic_simulation)

# Print the mesh
print(harmonic_simulation.mesh)

# Print the list of constructed geometries
print(harmonic_simulation.geometries)

# Print the list of boundary conditions
print(harmonic_simulation.boundary_conditions)

# Print the list of available named selections
named_selections = harmonic_simulation.named_selections
print(named_selections)

# Print available frequencies, phase angles, and RPMs
print(harmonic_simulation.time_freq_support)
print(harmonic_simulation.frequencies)
print(harmonic_simulation.phase_angles)
print(harmonic_simulation.rpms)

# Print the list of available results
print(harmonic_simulation.results)

# General plot of the simulation object with, by default:
# - the mesh, not deformed
# - the geometry
# - the boundary conditions
harmonic_simulation.plot(mesh=True, geometry=True, boundary_conditions=True)

# -----------------------------------------------------------------------------------------
# Apply a selection
selection = Selection()
selection.select_nodes(nodes=[1, 2, 3])
selection.select_time_freq_indices(time_freq_indices=[0, 1])
harmonic_simulation.activate_selection(selection_object=selection)

# Deactivate a selection
harmonic_simulation.deactivate_selection()

# -----------------------------------------------------------------------------------------
# Extract results

# Extract displacements along X for nodes 1, 2 and 3 at f=0.05Hz
displacement_X = harmonic_simulation.displacement(
    components=["X"], nodes=[1, 2, 3], frequencies=[0.05]
)
print(displacement_X)

# Extract nodal XY stresses for elements 1, 2 and 3 at set 1
stress_XY = harmonic_simulation.elemental_stress(
    components=["XY"], elements=[1, 2, 3], set_ids=[1]
)
print(stress_XY)

# Extract first principal nodal stress for a named (elemental or nodal) selection at all frequencies
stress_S1 = harmonic_simulation.nodal_principal_stress(
    components=["1"], named_selection=named_selections[0]
)
print(stress_S1)

# Extract equivalent elemental strain for a selection at set 1
strain_eqv = harmonic_simulation.elemental_eqv_strain(selection=selection, set_ids=[1])
print(strain_eqv)

# -----------------------------------------------------------------------------------------
# Extract the mesh
mesh = harmonic_simulation.mesh

# Show the mesh with defaults for harmonic:
# - not deformed
# (- at first frequency)
# (- at first phase angle (0°))
mesh.plot(opacity=0.3, title="Harmonic mesh plot", text="defaults to not deformed")

# Bode plot - Frequency response plot
# gives displacement and phase angle at location of peak response
