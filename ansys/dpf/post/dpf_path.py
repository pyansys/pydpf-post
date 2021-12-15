"""Module containing the DpfPath class that will
define a path of coordinates to set the result on.
"""
import numpy as np

from ansys.dpf.core.common import locations, natures
from ansys.dpf.core import Field

def create_path_on_coordinates(coordinates):
    """
    Create a dpf path object that can be used to request
    results on a specific path of coordinates.

    Parameters
    ----------
        coordinates : list[list[int]], Field, arrays
            3D coordinates.

    Example
    -------
    >>> from ansys.dpf import post
    >>> from ansys.dpf.post import examples
    >>> coordinates = [[0.024, 0.03, 0.003]]
    >>> for i in range(1, 51):
    ...     coord_copy = ref.copy()
    ...     coord_copy[1] = coord_copy[0] + i * 0.001
    ...     coordinates.append(coord_copy)
    >>> path_on_coord = post.create_path_on_coordinates(
    ... coordinates=coordinates
    ... )
    >>> solution = post.load_solution(examples.static_rst)
    >>> stress = solution.stress(path=dpf_path)

    """
    return DpfPath(coordinates=coordinates)

class DpfPath:
    """This object describe a set of coordinates."""

    def __init__(self, coordinates):
        """
        DpfPath object constructor.

        Parameters
        ----------
        coordinates : list[list[int]], Field, arrays
            3D coordinates.

        Example
        -------
        >>> coordinates = [[0.024, 0.03, 0.003]]
        >>> for i in range(1, 51):
        ...     coord_copy = ref.copy()
        ...     coord_copy[1] = coord_copy[0] + i * 0.001
        ...     coordinates.append(coord_copy)
        >>> dpf_path = post.DpfPath(coordinates=coordinates)

        """
        if isinstance(coordinates, Field):
            self._field = coordinates
        else:
            coord_length = len(coordinates)
            if isinstance(coordinates, list):
                if isinstance(coordinates[0], float):
                    coord_length /= 3
            elif isinstance(coordinates, (np.ndarray, np.generic)):
                if len(coordinates.shape) == 1:
                    coord_length /= 3
            self._field = Field(nature=natures.vector, location=locations.nodal)
            self._field.scoping.ids = list(range(1, int(coord_length) + 1))
            self._field.data = coordinates

    @property
    def coordinates(self):
        return self._field.data