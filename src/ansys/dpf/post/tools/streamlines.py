"""Module containing the helpers for streamlines.

Streamlines
-----------

"""
from typing import List, Union

from ansys.dpf.core.helpers import streamlines as core_streamlines
from ansys.dpf.core.plotter import DpfPlotter

from ansys.dpf import post


def plot_streamlines(
    dataframe: post.DataFrame,
    sources: List[dict],
    streamline_thickness: Union[float, List[float]] = 0.01,
    plot_mesh: bool = True,
    mesh_opacity: float = 0.3,
    plot_contour: bool = True,
    contour_opacity: float = 0.3,
    **kwargs,
):
    """Plot streamlines based on a vector field DataFrame.

    Parameters
    ----------
    dataframe:
        A `post.DataFrame` object containing a vector field.
    sources:
        A list of dictionaries defining spherical point sources for the streamlines.
        Expected keywords are "center", "radius", "max_time" and "n_points".
        Keyword "max_time" is for the maximum integration pseudo-time for the streamline
        computation algorithm, which defines the final length of the lines.
        More information is available at :func:`pyvista.DataSetFilters.streamlines`.
    streamline_thickness:
        Thickness of the streamlines plotted. Use a list to specify a value for each source.
    plot_contour:
        Whether to plot the field's norm contour along with the streamlines.
    contour_opacity:
        Opacity to use for the field contour in case "plot_contour=True".
    plot_mesh:
        Whether to plot the mesh along the streamlines in case "plot_contour=False".
    mesh_opacity:
        Opacity to use for the mesh in case "plot_contour=False" and "plot_mesh=True".
    **kwargs:

    """
    # Select data to work with
    meshed_region = dataframe._fc[0].meshed_region
    field = dataframe._fc[0]

    # Initialize the plotter
    plt = DpfPlotter(**kwargs)

    if plot_contour:
        plt.add_field(field=field, opacity=contour_opacity)
    elif plot_mesh:
        plt.add_mesh(meshed_region=meshed_region, opacity=mesh_opacity)
    if not isinstance(streamline_thickness, list):
        streamline_thickness = [streamline_thickness] * len(sources)
    # Add streamlines for each source
    for i, source in enumerate(sources):
        pv_streamline, pv_source = core_streamlines.compute_streamlines(
            meshed_region=meshed_region,
            field=field,
            return_source=True,
            source_radius=source["radius"],
            source_center=source["center"],
            n_points=source["n_points"] if "n_points" in source else 100,
            max_time=source["max_time"] if "max_time" in source else None,
        )
        plt.add_streamlines(
            pv_streamline, source=pv_source, radius=streamline_thickness[i]
        )

    plt.show_figure(**kwargs)
