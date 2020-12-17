"""This module contains the electric results class ."""

from ansys.dpf.post.scalar import Scalar
from ansys.dpf.post.vector import Vector
from ansys.dpf.core.common import locations
    
    
class ElectricField(Vector):
    """Defines the temperature object for thermal/electric analysis, that is a scalar object."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._operator_name = "EF"
        
        if self.definition.location == locations.nodal:
            self._op_average = "to_nodal_fc"
        if self.definition.location == locations.elemental:
            self._op_average = "to_elemental_fc"
        self.definition.location = None
        self.definition._Definition__location_locked = True
            

    def __str__(self):
        txt = super().__str__()
        txt += "\n"
        txt += "This is an electric field object."
        return txt
    
    
class ElectricPotential(Scalar):
    """Defines the temperature object for thermal/electric analysis, that is a scalar object."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._operator_name = "VOLT"

    def __str__(self):
        txt = super().__str__()
        txt += "\n"
        txt += "This is an electric potential object."
        return txt