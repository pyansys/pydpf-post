import numpy as np
import pytest
from pytest import fixture

from ansys.dpf import core as dpf
from ansys.dpf import post
from ansys.dpf.post import examples
from ansys.dpf.post.selection import SpatialSelection, _WfNames
from conftest import SERVERS_VERSION_GREATER_THAN_OR_EQUAL_TO_7_0


def test_spatial_selection_select_nodes(allkindofcomplexity):
    simulation = post.load_simulation(allkindofcomplexity)
    selection = SpatialSelection()
    selection._selection.progress_bar = False
    selection.select_nodes([1, 2, 3])
    scoping = selection._evaluate_on(simulation)
    assert scoping.location == post.locations.nodal
    assert np.allclose(scoping.ids, [1, 2, 3])


def test_spatial_selection_select_elements(allkindofcomplexity):
    simulation = post.load_simulation(allkindofcomplexity)
    selection = SpatialSelection()
    selection._selection.progress_bar = False
    selection.select_elements([1, 2, 3, 4])
    scoping = selection._evaluate_on(simulation)
    assert scoping.location == post.locations.elemental
    assert np.allclose(scoping.ids, [1, 2, 3, 4])
    ids = selection.apply_to(simulation)
    assert np.allclose(ids, [1, 2, 3, 4])


def test_spatial_selection_select_named_selection(allkindofcomplexity):
    simulation = post.load_simulation(allkindofcomplexity)
    selection = SpatialSelection()
    selection._selection.progress_bar = False
    selection.select_named_selection(
        simulation.mesh.named_selections.keys()[0],
        location=post.selection.locations.nodal,
    )
    scoping = selection._evaluate_on(simulation)
    assert scoping.location == post.locations.nodal
    assert scoping.ids.size == 12970
    assert 1857 in scoping.ids
    assert 14826 in scoping.ids
    ids = selection.apply_to(simulation)
    assert len(ids) == 12970
    assert 1857 in ids
    assert 14826 in ids


def test_spatial_selection_select_skin(static_rst):
    simulation = post.StaticMechanicalSimulation(static_rst)
    selection = SpatialSelection()
    selection._selection.progress_bar = False
    selection.select_skin(
        location=post.locations.elemental_nodal,
        result_native_location=post.locations.elemental_nodal,
        elements=[1, 2, 3],
    )
    mesh_wf = dpf.Workflow()
    mesh_wf.set_output_name(
        _WfNames.initial_mesh, simulation._model.metadata.mesh_provider
    )
    selection._selection.connect_with(
        mesh_wf,
        output_input_names={_WfNames.initial_mesh: _WfNames.initial_mesh},
    )
    # This returns a scoping on the initial mesh (logic to change?)
    scoping_ids = selection.apply_to(simulation)
    assert len(scoping_ids) == 8

    # This gives the skin mesh with its 9 shell elements
    skin = selection._selection.get_output(_WfNames.skin, dpf.MeshedRegion)
    assert len(skin.elements.scoping.ids) == 9


@pytest.mark.skipif(
    not SERVERS_VERSION_GREATER_THAN_OR_EQUAL_TO_7_0,
    reason="Faces added with ansys-dpf-server 2024.1.pre0.",
)
class TestSpatialSelectionFaces:
    @fixture
    def fluent_simulation(self):
        fluid_example_files = examples.download_fluent_axial_comp()
        ds = dpf.DataSources()
        ds.set_result_file_path(
            fluid_example_files["cas"][0],
            key="cas",
        )
        ds.add_file_path(
            fluid_example_files["dat"][0],
            key="dat",
        )
        return post.FluidSimulation(ds)  # noqa

    def test_spatial_selection_select_faces(self, fluent_simulation):
        selection = SpatialSelection()
        selection._selection.progress_bar = False
        selection.select_faces(fluent_simulation.mesh.face_ids)
        scoping = selection._evaluate_on(fluent_simulation)
        assert scoping.location == post.locations.faces
        assert np.allclose(scoping.ids, fluent_simulation.mesh.face_ids)

    def test_spatial_selection_select_nodes_of_faces(self, fluent_simulation):
        selection = SpatialSelection()
        selection._selection.progress_bar = False
        face_0 = fluent_simulation.mesh.faces[0]
        selection.select_nodes_of_faces(
            faces=[face_0.id],
            mesh=fluent_simulation.mesh,
        )
        scoping = selection._evaluate_on(fluent_simulation)
        assert scoping.location == post.locations.nodal
        assert np.allclose(scoping.ids, face_0.node_ids)

    def test_spatial_selection_select_faces_of_elements(self, fluent_simulation):
        selection = SpatialSelection()
        selection._selection.progress_bar = False
        elem_0 = fluent_simulation.mesh.elements[0]
        selection.select_faces_of_elements(
            elements=[elem_0.id],
            mesh=fluent_simulation.mesh,
        )
        scoping = selection._evaluate_on(fluent_simulation)
        assert scoping.location == post.locations.faces
        assert np.allclose(scoping.ids, [11479, 11500, -1, 11502, 11503])


#
#
# def test_spatial_selection_intersect(allkindofcomplexity):
#     solution = post.load_solution(allkindofcomplexity, legacy=False)
#     selection1 = SpatialSelection()
#     selection1.select_nodes([1, 2, 3])
#     _ = selection1._evaluate_on(solution)
#
#     selection = SpatialSelection()
#     selection.select_nodes([1, 2, 3, 4])
#     selection.intersect(selection1)
#     scoping = selection._evaluate_on(solution)
#     assert scoping.location == post.selection.locations.nodal
#     assert np.allclose(scoping.ids, [1, 2, 3])
#     ids = selection.apply_to(solution)
#     assert np.allclose(ids, [1, 2, 3])
