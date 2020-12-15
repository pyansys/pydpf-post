from ansys.dpf.post.electric_results import ElectricField, ElectricPotential
from ansys.dpf.post.common import _PhysicsType
from ansys.dpf import post
import numpy as np
import unittest
import pytest

filepath = "d:/rst/rth_electric.rth"


def test_electricfield():
    solution = post.load_solution(filepath)
    assert solution._model.metadata.result_info.physics_type == _PhysicsType.thermal
    ef = solution.electric_field()
    assert isinstance(ef, ElectricField)
    s = ef.vector
    assert s.num_fields == 1
    assert s[0].location == post.locations.nodal
    assert len(s[0].data[20]) == 3
    assert np.isclose(s[0].data[23][1], 19.562952041625977)


def test_electricfield_nodscoping():
    solution = post.load_solution(filepath)
    ef = solution.electric_field(node_scoping = [2])
    s = ef.vector
    assert s.num_fields == 1
    assert s[0].location == post.locations.nodal
    assert len(s[0].data) == 20
    assert len(s[0].data[0]) == 3
    assert np.allclose(s[0].data[0].tolist(), [2.63128894e-11, 1.95629520e+01, 2.62733394e-11])
    ef = solution.electric_field(location = post.locations.elemental, node_scoping = [2])
    s = ef.vector
    assert s.num_fields == 1
    assert s[0].location == post.locations.elemental
    assert len(s[0].data[0]) == 3
    assert np.allclose(s[0].data.tolist(), [-3.41948692e-14,  1.95629520e+01,  7.77156117e-15])
    ef = solution.electric_field(location = post.locations.elemental_nodal, node_scoping = [2])
    s = ef.vector
    assert s.num_fields == 1
    assert s[0].location == post.locations.elemental_nodal
    assert len(s[0].data) == 8
    assert len(s[0].data[0]) == 3
    assert np.allclose(s[0].data.tolist(), [-3.41948692e-14,  1.95629520e+01,  7.77156117e-15])


def test_electricfield_elemscoping():
    raise Exception("Element scoping on electric_field does not work.")
    solution = post.load_solution(filepath)
    ef = solution.electric_field(element_scoping = [2])
    s = ef.vector
    assert s.num_fields == 1
    assert s[0].location == post.locations.nodal
    assert len(s[0].data) == 20
    assert len(s[0].data[0]) == 3
    #assert np.isclose(s[0].data[0].tolist(), [2.63128894e-11, 1.95629520e+01, 2.62733394e-11])
    ef = solution.electric_field(location = post.locations.elemental, element_scoping = [2])
    s = ef.vector
    assert s.num_fields == 1
    assert s[0].location == post.locations.elemental
    assert len(s[0].data) == 3
    #assert np.isclose(s[0].data.tolist(), [-3.41948692e-14,  1.95629520e+01,  7.77156117e-15])
    ef = solution.electric_field(location = post.locations.elemental_nodal, element_scoping = [2])
    s = ef.vector
    assert s.num_fields == 1
    assert s[0].location == post.locations.elemental_nodal
    assert len(s[0].data) == 8
    assert len(s[0].data[0]) == 3
    #assert np.isclose(s[0].data.tolist(), [-3.41948692e-14,  1.95629520e+01,  7.77156117e-15])


def test_electricfield_nodlocation():
    solution = post.load_solution(filepath)
    ef = solution.electric_field()
    s = ef.vector
    assert s.num_fields == 1
    assert s[0].location == post.locations.nodal


class TestCase1(unittest.TestCase):
    
    @pytest.fixture(autouse=True)
    def set_filepath(self, allkindofcomplexity):
        self._filepath = filepath
        
    def test_electricpotential_changelocation(self):
        solution = post.load_solution(self._filepath)
        pot = solution.electric_potential(location = post.locations.elemental)
        self.assertRaises(Exception, pot.definition.location, post.locations.nodal)


def test_electricfield_elemlocation():
    solution = post.load_solution(filepath)
    ef = solution.electric_field(location = post.locations.elemental)
    s = ef.vector
    assert s.num_fields == 1
    assert s[0].location == post.locations.elemental


def test_electricfield_elemnodlocation():
    solution = post.load_solution(filepath)
    ef = solution.electric_field(location = post.locations.elemental_nodal)
    s = ef.vector
    assert s.num_fields == 1
    assert s[0].location == post.locations.elemental_nodal


def test_electricfield_timescoping():
    solution = post.load_solution(filepath)
    ef = solution.electric_field(time_scoping = 1)
    s = ef.vector
    assert s.num_fields == 1
    assert s[0].location == post.locations.nodal
    assert len(s[0].data[20]) == 3
    assert np.isclose(s[0].data[23][1], 19.562952041625977)


def test_electricfield_time():
    solution = post.load_solution(filepath)
    ef = solution.electric_field(time = 1.)
    s = ef.vector
    assert s.num_fields == 1
    assert s[0].location == post.locations.nodal
    assert len(s[0].data[20]) == 3
    assert np.isclose(s[0].data[23][1], 19.562952041625977)


def test_electricfield_set():
    solution = post.load_solution(filepath)
    ef = solution.electric_field(set = 1)
    s = ef.vector
    assert s.num_fields == 1
    assert s[0].location == post.locations.nodal
    assert len(s[0].data[20]) == 3
    assert np.isclose(s[0].data[23][1], 19.562952041625977)



def test_electricpotential():
    solution = post.load_solution(filepath)
    assert solution._model.metadata.result_info.physics_type == _PhysicsType.thermal
    ef = solution.electric_potential()
    assert isinstance(ef, ElectricPotential)
    s = ef.scalar
    assert s.num_fields == 1
    assert s[0].location == post.locations.nodal
    assert len(s[0].data) == 4125
    assert np.isclose(s[0].data[23], 0.09781476007338061)
    

to_return = "node scoping and element scoping returns the same"
def test_electricpotential_nodscoping():
    solution = post.load_solution(filepath)
    ef = solution.electric_potential(node_scoping = [2])
    s = ef.scalar
    assert s.num_fields == 1
    assert s[0].location == post.locations.nodal
    assert len(s[0].data) == 1
    assert np.isclose(s[0].data[0], 0.048907380036668786)


def test_electricpotential_elemscoping():
    solution = post.load_solution(filepath)
    ef = solution.electric_potential(node_scoping = [2])
    s = ef.scalar
    assert s.num_fields == 1
    assert s[0].location == post.locations.nodal
    assert len(s[0].data) == 1
    #assert np.isclose(s[0].data[0], 0.02445369)
    raise Exception(to_return)


def test_electricpotential_nodlocation():
    solution = post.load_solution(filepath)
    ef = solution.electric_potential(location = post.locations.nodal)
    s = ef.scalar
    assert s.num_fields == 1
    assert s[0].location == post.locations.nodal


class TestCase2(unittest.TestCase):
    
    @pytest.fixture(autouse=True)
    def set_filepath(self, allkindofcomplexity):
        self._filepath = filepath
        
    def test_electricpotential_elemlocation(self):
        solution = post.load_solution(self._filepath)
        pot = solution.electric_potential(location = post.locations.elemental)
        self.assertRaises(Exception, s = pot.scalar)
    
    def test_electricpotential_elemnodallocation(self):
        solution = post.load_solution(self._filepath)
        pot = solution.electric_potential(location = post.locations.elemental_nodal)
        self.assertRaises(Exception, s = pot.scalar)


def test_electricpotential_timescoping():
    solution = post.load_solution(filepath)
    ef = solution.electric_potential(time_scoping = [1])
    s = ef.scalar
    assert s.num_fields == 1
    assert len(s[0].data) == 4125
    assert s[0].location == post.locations.nodal
    assert np.isclose(s[0].data[0], 0.07336107005500624)


def test_electricpotential_time():
    solution = post.load_solution(filepath)
    ef = solution.electric_potential(set = 1)
    s = ef.scalar
    assert s.num_fields == 1
    assert len(s[0].data) == 4125
    assert s[0].location == post.locations.nodal
    assert np.isclose(s[0].data[0], 0.07336107005500624)


def test_electricpotential_set():
    solution = post.load_solution(filepath)
    ef = solution.electric_potential(time = 1.)
    s = ef.scalar
    assert s.num_fields == 1
    assert len(s[0].data) == 4125
    assert s[0].location == post.locations.nodal
    assert np.isclose(s[0].data[0], 0.07336107005500624)