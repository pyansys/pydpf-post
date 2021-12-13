import os
import numpy as np
import pytest

from ansys import dpf
from ansys.dpf import post
from ansys.dpf.post.result_data import ResultData
from ansys.dpf.core.common import locations

# currently running dpf on docker.  Used for testing on CI
RUNNING_DOCKER = os.environ.get("DPF_DOCKER", False)


def test_num_fields_verbose_api(allkindofcomplexity):
    result = post.load_solution(allkindofcomplexity)
    disp = result.misc.nodal_displacement()
    assert isinstance(disp, ResultData)
    assert disp.num_fields == 1


def test_num_fields(allkindofcomplexity):
    result = post.load_solution(allkindofcomplexity)
    d = result.displacement()
    disp = d.vector
    assert isinstance(disp, ResultData)
    assert disp.num_fields == 1


def test_data_at_field_verbose_api(allkindofcomplexity):
    result = post.load_solution(allkindofcomplexity)
    disp = result.misc.nodal_displacement()
    data = disp.get_data_at_field(0)
    assert len(data) == 15113
    assert len(data[0]) == 3


def test_data_at_field(allkindofcomplexity):
    result = post.load_solution(allkindofcomplexity)
    d = result.displacement()
    disp = d.vector
    data = disp.get_data_at_field(0)
    assert len(data) == 15113
    assert len(data[0]) == 3


def test_field_getitem_verbose_api(allkindofcomplexity):
    result = post.load_solution(allkindofcomplexity)
    disp = result.misc.nodal_displacement()
    field = disp[0]
    assert isinstance(field, dpf.core.Field)
    assert field.location == locations.nodal


def test_field_getitem(allkindofcomplexity):
    result = post.load_solution(allkindofcomplexity)
    d = result.displacement()
    disp = d.vector
    field = disp[0]
    assert isinstance(field, dpf.core.Field)
    assert field.location == locations.nodal


def test_max_verbose_api(allkindofcomplexity):
    result = post.load_solution(allkindofcomplexity)
    disp = result.misc.nodal_displacement()
    max_val = disp.max
    assert len(max_val) == 3
    assert len(max_val.data) == 1
    assert len(max_val.data[0]) == 3


def test_max(allkindofcomplexity):
    result = post.load_solution(allkindofcomplexity)
    d = result.displacement()
    disp = d.vector
    max_val = disp.max
    assert len(max_val) == 3
    assert len(max_val.data) == 1
    assert len(max_val.data[0]) == 3


def test_min_verbose_api(allkindofcomplexity):
    result = post.load_solution(allkindofcomplexity)
    disp = result.misc.nodal_displacement()
    min_val = disp.min
    assert len(min_val) == 3
    assert len(min_val.data) == 1
    assert len(min_val.data[0]) == 3


def test_min(allkindofcomplexity):
    result = post.load_solution(allkindofcomplexity)
    d = result.displacement()
    disp = d.vector
    min_val = disp.min
    assert len(min_val) == 3
    assert len(min_val.data) == 1
    assert len(min_val.data[0]) == 3


def test_maxdata_verbose_api(allkindofcomplexity):
    result = post.load_solution(allkindofcomplexity)
    disp = result.misc.nodal_displacement()
    val = disp.max_data
    assert len(val) == 1
    assert len(val[0]) == 3


def test_maxdata(allkindofcomplexity):
    result = post.load_solution(allkindofcomplexity)
    d = result.displacement()
    disp = d.vector
    val = disp.max_data
    assert len(val) == 1
    assert len(val[0]) == 3


def test_mindata_verbose_api(allkindofcomplexity):
    result = post.load_solution(allkindofcomplexity)
    disp = result.misc.nodal_displacement()
    val = disp.min_data
    assert len(val) == 1
    assert len(val[0]) == 3


def test_mindata(allkindofcomplexity):
    result = post.load_solution(allkindofcomplexity)
    d = result.displacement()
    disp = d.vector
    val = disp.min_data
    assert len(val) == 1
    assert len(val[0]) == 3


def test_maxdata_at_field_verbose_api(allkindofcomplexity):
    result = post.load_solution(allkindofcomplexity)
    disp = result.misc.nodal_displacement()
    val = disp.get_max_data_at_field(0)
    assert len(val) == 3


def test_maxdata_at_field(allkindofcomplexity):
    result = post.load_solution(allkindofcomplexity)
    d = result.displacement()
    disp = d.vector
    val = disp.get_max_data_at_field(0)
    assert len(val) == 3


def test_min_data_at_field_verbose_api(allkindofcomplexity):
    result = post.load_solution(allkindofcomplexity)
    disp = result.misc.nodal_displacement()
    val = disp.get_min_data_at_field(0)
    assert len(val) == 3


def test_min_data_at_field(allkindofcomplexity):
    result = post.load_solution(allkindofcomplexity)
    d = result.displacement()
    disp = d.vector
    val = disp.get_min_data_at_field(0)
    assert len(val) == 3


def test_get_all_labels_verbose_api(modalallkindofcomplexity):
    result = post.load_solution(modalallkindofcomplexity)
    stress = result.misc.elemental_stress()
    l = [{"elshape": 1, "time": 1}, {"elshape": 0, "time": 1}]
    l_comp = stress.get_all_label_spaces()
    assert l == l_comp


def test_get_all_labels(modalallkindofcomplexity):
    result = post.load_solution(modalallkindofcomplexity)
    s = result.stress(location=post.locations.elemental)
    stress = s.tensor
    l = [{"elshape": 1, "time": 1}, {"elshape": 0, "time": 1}]
    l_comp = stress.get_all_label_spaces()
    assert l == l_comp


def test_get_scoping_at_field_verbose_api(plate_msup):
    result = post.load_solution(plate_msup)
    disp = result.misc.nodal_displacement(time_scoping=[1, 2, 4])
    assert disp.num_fields == 3
    scop = disp.get_scoping_at_field(2)
    assert len(scop) == 393
    assert scop[2] == 95


def test_get_scoping_at_field(plate_msup):
    result = post.load_solution(plate_msup)
    d = result.displacement(time_scoping=[1, 2, 4])
    disp = d.vector
    assert disp.num_fields == 3
    scop = disp.get_scoping_at_field(2)
    assert len(scop) == 393
    assert scop[2] == 95


def test_print(plate_msup):
    result = post.load_solution(plate_msup)
    print(result)
    d = result.displacement(time_scoping=[1, 2, 4])
    print(d)
    disp = d.vector
    print(disp)


def test_plot_chart(plate_msup):
    transient_sol = post.load_solution(plate_msup)
    disp = transient_sol.displacement(time_scoping=list(range(1, 21)))
    vector = disp.vector
    vector.num_fields
    vector._plot_chart()


def test_plot_contour_one_field(plate_msup):
    solution = post.load_solution(plate_msup)
    stress = solution.stress(location=post.locations.elemental, time_scoping=[1])
    s = stress.tensor
    s.plot_contour("time", 1)
    s.plot_contour()


def test_plot_contour_two_fields(allkindofcomplexity):
    # split shell/solid
    solution = post.load_solution(allkindofcomplexity)
    stress = solution.stress(location=post.locations.elemental, time_scoping=[1])
    s = stress.tensor
    s.plot_contour("time", 1)
    s.plot_contour()


def test_plot_contour_with_keys(allkindofcomplexity):
    result = post.load_solution(allkindofcomplexity)
    d = result.displacement(grouping=post.grouping.by_el_shape)
    disp = d.vector
    disp.plot_contour("elshape", 1)

    d = result.displacement(grouping=post.grouping.by_material)
    disp = d.vector
    disp.plot_contour("mat", 1)

    s = result.stress(
        grouping=post.grouping.by_el_shape, location=post.locations.elemental
    )
    stress = s.tensor
    stress.plot_contour("elshape", 1)

    s = result.stress(
        grouping=post.grouping.by_material, location=post.locations.elemental
    )
    stress = s.tensor
    stress.plot_contour("mat", 1)


@pytest.mark.skipif(RUNNING_DOCKER, reason="Path hidden within docker container")
def test_plot_with_vtk_file(allkindofcomplexity):
    solution = post.load_solution(allkindofcomplexity)
    stress = solution.stress(location=post.locations.elemental, time_scoping=[1])
    s = stress.tensor
    s._plot_contour_with_vtk_file()

from ansys.dpf import core
version_core = core.__version__
MEETS_CORE_034 = core.check_version.meets_version(version_core, '0.3.4')
@pytest.mark.skipif(not MEETS_CORE_034, reason="Plot path on coordinates"
                    "available from dpf-core 0.3.4.")
def test_plot_on_coordinates(model_ns):
    coordinates = [[-0.0195, 0.006, -0.0025]]
    for i in range(1, 101):
        coord_copy = []
        coord_copy.append(coordinates[0][0])
        coord_copy.append(coordinates[0][1])
        coord_copy.append(coordinates[0][2])
        coord_copy[0] = coord_copy[0] + i * 0.0003
        coordinates.append(coord_copy)
    ref = [-0.0155, 0.00600634, -0.0025]
    coordinates.append(ref)
    for i in range(1, 101):
        coord_copy = []
        coord_copy.append(ref[0])
        coord_copy.append(ref[1])
        coord_copy.append(ref[2])
        coord_copy[0] = coord_copy[0] + i * 0.0003
        coordinates.append(coord_copy)
    ref = [-0.0125, 0.00600507, -0.0025]
    coordinates.append(ref)
    for i in range(1, 101):
        coord_copy = []
        coord_copy.append(ref[0])
        coord_copy.append(ref[1])
        coord_copy.append(ref[2])
        coord_copy[0] = coord_copy[0] + i * 0.0003
        coordinates.append(coord_copy)
    ref = [-0.0125, 0.00600444, -0.0025]
    coordinates.append(ref)
    for i in range(1, 101):
        coord_copy = []
        coord_copy.append(ref[0])
        coord_copy.append(ref[1])
        coord_copy.append(ref[2])
        coord_copy[0] = coord_copy[0] + i * 0.0003
        coordinates.append(coord_copy)
    solution = post.load_solution(model_ns)
    path = post.create_path_on_coordinates(coordinates=coordinates)
    displacement = solution.displacement(path=path)
    displacement.vector.plot_contour(notebook=False)

@pytest.mark.skipif(not MEETS_CORE_034, reason="Path on coordinates"
                    "available from dpf-core 0.3.4.")
def test_path_on_coordinates_with_scoping(static_rst):
    coordinates = [[0.024, 0.03, 0.003]]
    for i in range(1, 3):
        coord_copy = coordinates[0].copy()
        coord_copy[1] = coord_copy[0] + i * 0.01
        coordinates.append(coord_copy)
    solution = post.load_solution(static_rst)
    scoping_ids_orig = [14, 5, 101]
    path = post.create_path_on_coordinates(coordinates=coordinates,
                                           scoping=scoping_ids_orig)
    displacement = solution.displacement(path=path)
    vector = displacement.vector
    field = vector.result_fields_container[0]
    assert len(field) == 9 # 3 notes * 3 dofs
    assert len(field.scoping) == 3
    scoping_ids = field.scoping.ids
    result = np.array_equal(np.array(scoping_ids).sort(),
                            np.array(scoping_ids_orig).sort())
    assert result is True