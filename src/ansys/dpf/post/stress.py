# Copyright (C) 2020 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""This module contains classes for stress results."""

from ansys.dpf.post.result_object import Result
from ansys.dpf.post.tensor import ComplexTensor, Tensor


class Stress(Tensor):
    """Defines the stress object, which is a tensor object.

    Examples
    --------
    Extract the stress from a solution.

    >>> from ansys.dpf import post
    >>> from ansys.dpf.post import examples
    >>> solution = post.load_solution(examples.multishells_rst)
    >>> stress = solution.stress(location=post.locations.nodal, time_scoping=[1])
    """

    def __init__(self, **kwargs):
        """Initialize this class."""
        super().__init__(**kwargs)
        self._operator_name = "S"

    def __str__(self):
        """Return the string representation of this class."""
        return f"Stress {super().__str__()}"

    @property
    def von_mises(self):
        """Result data for the von Mises stress."""
        return super()._get_result_data("S_eqv", self._data_sources, self._model)


class ComplexStress(ComplexTensor, Stress):
    """Defines the complex tensor stress object."""

    def __init__(self, **kwargs):
        """Initialize this class."""
        super().__init__(**kwargs)
        self._operator_name = "S"

    def __str__(self):
        """Return the string representation of this class."""
        return f"Complex stress.\n{super().__str__()}"

    @property
    def von_mises_amplitude(self):
        """Amplitude for the von Mises stress."""
        res_data = super()._get_result_data("S_eqv", self._data_sources, self._model)
        return Result._get_amplitude_evaluation(self, res_data)

    def von_mises_at_phase(self, phase: float):
        """Get the von Mises stress at a specific phase."""
        return super()._get_result_data(
            "S_eqv", self._data_sources, self._model, phase=phase
        )
