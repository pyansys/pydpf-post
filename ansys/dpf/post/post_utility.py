"""Module containing the method to instantiate the result
object. Initialization of post objects.
"""
from builtins import Exception

from ansys.dpf.core.model import Model

from ansys.dpf.post.common import _AnalysisType, _AvailableKeywords, _PhysicsType
from ansys.dpf.post.static_analysis import (
    StaticAnalysisSolution,
    ThermalStaticAnalysisSolution,
)
from ansys.dpf.post.modal_analysis import ModalAnalysisSolution
from ansys.dpf.post.harmonic_analysis import HarmonicAnalysisSolution
from ansys.dpf.post.transient_analysis import (
    TransientAnalysisSolution,
    ThermalTransientAnalysisSolution,
)


def load_solution(data_sources, physics_type=None, analysis_type=None):
    """Return a ``Result`` object which can provide information on a given
    set, on a given scoping.

    Parameters
    ----------
    data_sources : str or dpf.core.DataSources
         filepath to the file you want to open, or a dpf.core.DataSources().

    physics_type : common._PhysicsType, str, optional
        ["mecanic", "thermal"] optionally specify the type of physics described in
        the ''data_sources''. If nothing is specified, the ''data_sources'' are
        read to evaluate the ''physics_type''.

    analysis_type : common._AnalysisType, str, optional
        ["static", "modal", "harmonic", "transient"] optionally specify the type of
        analysis described in the ''data_sources''.
        If nothing is specified, the ''data_sources'' are read to evaluate
        the ''analysis_type''.

    Examples
    --------
    >>> from ansys.dpf import post
    >>> from ansys.dpf.post import examples
    >>> solution = post.load_solution(examples.static_rst)
    """
    _model = Model(data_sources)
    data_sources = _model.metadata.data_sources

    if not physics_type:
        try:
            physics_type = _model.metadata.result_info.physics_type
        except Exception as e:
            print("Physics type is taken as mecanic by default, please specify physics_type",
                  "keyword if it's wrong")
            physics_type = _PhysicsType.mecanic

    if not analysis_type:
        try:
            analysis_type = _model.metadata.result_info.analysis_type
        except Exception as e:
            print("Analysis type is taken as static by default, please specify analysis_type",
                  "keyword if it's wrong")
            analysis_type = _AnalysisType.static

    if physics_type == _PhysicsType.thermal:
        if analysis_type == _AnalysisType.static:
            return ThermalStaticAnalysisSolution(data_sources, _model)
        elif analysis_type == _AnalysisType.transient:
            return ThermalTransientAnalysisSolution(data_sources, _model)
        else:
            raise Exception(f"Unknown analysis type '{analysis_type}' for thermal.")
    elif physics_type == _PhysicsType.mecanic:
        if analysis_type == _AnalysisType.static:
            return StaticAnalysisSolution(data_sources, _model)
        elif analysis_type == _AnalysisType.modal:
            return ModalAnalysisSolution(data_sources, _model)
        elif analysis_type == _AnalysisType.harmonic:
            return HarmonicAnalysisSolution(data_sources, _model)
        elif analysis_type == _AnalysisType.transient:
            return TransientAnalysisSolution(data_sources, _model)
        else:
            raise Exception(f"Unknown analysis type '{analysis_type}' for mechanical.")
    else:
        raise Exception(f"Unknown physics type '{physics_type}.")


def print_available_keywords():
    """Print the keywords that can be used into the result object.

    Examples
    --------
    >>> from ansys.dpf import post
    >>> solution = post.load_solution('file.rst')
    >>> post.print_available_keywords()
    """
    txt = _AvailableKeywords().__str__()
    print(txt)
