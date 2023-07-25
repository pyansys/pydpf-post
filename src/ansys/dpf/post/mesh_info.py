"""Module containing the ``FluidMeshInfo`` class.

FluidMeshInfo
-------------

"""
from ansys.dpf import core as dpf


class FluidMeshInfo:
    """Holds the metadata relative to a fluid mesh.

    This class describes the available mesh information.
    Use this to gather information about a big mesh prior to loading it
    to define requests on limited parts of the mesh for improved performance.

    Parameters
    ----------
    core_mesh_info :
        Hold the information of the mesh region into a generic data container.

    Examples
    --------
    Explore the mesh info from the model

    >>> from ansys.dpf import post
    >>> from ansys.dpf.post import examples
    >>> files = examples.download_fluent_axial_comp()
    >>> simulation = post.FluidSimulation(cas=files['cas'][0], dat=files['dat'][0])
    >>> mesh_info = simulation.mesh_info
    >>> print(mesh_info)  # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    Fluid mesh metadata
    -------------------
    Number of nodes: 16660
    Number of faces: 45391
    Number of cells: 13856
    Zones:
    """

    def __init__(self, core_mesh_info: dpf.MeshInfo):
        """Initialize this class."""
        self._core_object = core_mesh_info
        self._face_zones = None
        self._cell_zones = None

    def __str__(self) -> str:
        """String representation of this class."""
        txt = "Fluid mesh metadata\n"
        txt += "-" * (len(txt) - 1) + "\n"
        txt += f"Number of nodes: {self.num_nodes}\n"
        txt += f"Number of faces: {self.num_faces}\n"
        txt += f"Number of cells: {self.num_cells}\n"
        txt += "Zones:\n"
        return txt

    @property
    def num_nodes(self) -> int:
        """Returns the number of nodes in the mesh.

        Examples
        --------
        Get the number of nodes in the mesh

        >>> from ansys.dpf import post
        >>> from ansys.dpf.post import examples
        >>> files = examples.download_fluent_axial_comp()
        >>> simulation = post.FluidSimulation(cas=files['cas'][0], dat=files['dat'][0])
        >>> mesh_info = simulation.mesh_info
        >>> print(mesh_info.num_nodes)
        16660
        """
        return self._core_object.number_nodes

    @property
    def num_faces(self) -> int:
        """Returns the number of faces in the mesh.

        Examples
        --------
        Get the number of faces in the mesh

        >>> from ansys.dpf import post
        >>> from ansys.dpf.post import examples
        >>> files = examples.download_fluent_axial_comp()
        >>> simulation = post.FluidSimulation(cas=files['cas'][0], dat=files['dat'][0])
        >>> mesh_info = simulation.mesh_info
        >>> print(mesh_info.num_faces)
        45391
        """
        return self._core_object.number_faces

    @property
    def num_cells(self) -> int:
        """Returns the number of cells in the mesh.

        Examples
        --------
        Get the number of cells in the mesh

        >>> from ansys.dpf import post
        >>> from ansys.dpf.post import examples
        >>> files = examples.download_fluent_axial_comp()
        >>> simulation = post.FluidSimulation(cas=files['cas'][0], dat=files['dat'][0])
        >>> mesh_info = simulation.mesh_info
        >>> print(mesh_info.num_cells)
        13856
        """
        return self._core_object.number_elements

    @property
    def face_zones(self) -> dict:
        """Returns a dictionary of face zones in the mesh.

        Examples
        --------
        Get information on the face zones available in the mesh

        >>> from ansys.dpf import post
        >>> from ansys.dpf.post import examples
        >>> files = examples.download_fluent_axial_comp()
        >>> simulation = post.FluidSimulation(cas=files['cas'][0], dat=files['dat'][0])
        >>> mesh_info = simulation.mesh_info
        >>> print(mesh_info.face_zones)  # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
        {2: 'default-interior:0', 3: 'rotor-hub', ...26: 'stator-per-1', 27: 'stator-per-1-shadow'}
        """
        if not self._face_zones:
            zones = {}
            string_field = self._core_object.get_property("face_zone_names")
            for zone_id in string_field.scoping.ids:
                zone_name = string_field.get_entity_data_by_id(zone_id)[0]
                zones[zone_id] = zone_name
            self._face_zones = zones
        return self._face_zones

    @property
    def cell_zones(self) -> dict:
        """Returns a dictionaty of cell zones (bodies) in the mesh.

        Examples
        --------
        Get information on the cell zones available in the mesh

        >>> from ansys.dpf import post
        >>> from ansys.dpf.post import examples
        >>> files = examples.download_fluent_axial_comp()
        >>> simulation = post.FluidSimulation(cas=files['cas'][0], dat=files['dat'][0])
        >>> mesh_info = simulation.mesh_info
        >>> print(mesh_info.cell_zones)  # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
        {13: 'fluid-rotor', 28: 'fluid-stator'}
        """
        if not self._cell_zones:
            zones = {}
            string_field = self._core_object.body_names
            for zone_id in string_field.scoping.ids:
                zone_name = string_field.get_entity_data_by_id(zone_id)[0]
                zones[zone_id] = zone_name
            self._cell_zones = zones
        return self._cell_zones
