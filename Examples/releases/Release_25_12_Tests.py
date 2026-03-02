import hashlib
import math
from os import path

import pytest
from aspose.gis import Drivers, VectorLayer, Driver, Extent, Dataset, AbstractPath, DynamicFeature, NodeLink, \
    FeatureAttribute, AttributeDataType
from aspose.gis.formats.filegdb import FileGdbOptions
from aspose.gis.formats.geojson import GeoJsonOptions, GeoJsonLayer
from aspose.gis.formats.geopackage import GeoPackageOptions, GeoPackageDataset, GeoPackageTileMatrixSet, \
    GeoPackageTileOptions
from aspose.gis.formats.kml import KmlOptions, KmlLayer

from aspose.gis.geometries import Point, GeometryType, LineString, LinearRing, Polygon, Geometry
from aspose.gis.geotools import GeneratorTiles, GeneratorTilesRenderOptions
from aspose.gis.spatialreferencing import SpatialReferenceSystem
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

class Release_25_12_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Support Reading Extended GeoJson Tags
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-57
    # https://issue.saltov.dynabic.com/issues/GISNET-1928
    def GISNET1928Test(self):
        input_path = self.GetFileInBaseFolder("custom_field.json")
        source_path = AbstractPath.from_local_path(input_path)

        with Drivers.geo_json.open_as_geo_json_layer(source_path, GeoJsonOptions()) as layr:
            layer = cast(GeoJsonLayer, layr)
            # Assert "Geodata of Moscow" is the value of the "name" node
            assert layer.root.get_node_by_name("name").node_value == "Geodata of Moscow"

            # Get the "metadata" node and its children
            node_with_children = layer.get_node_by_name("metadata")
            look_at_children = node_with_children.children

            # Assert there are 4 children
            assert len(list(look_at_children)) == 4

            # Assert values of specific metadata fields
            assert node_with_children.find_node_by_name("creator").node_value == "GIS Department"
            assert node_with_children.find_node_by_name("created").node_value == "2024-01-15"
            assert node_with_children.find_node_by_name("version").node_value == "1.0"
            assert node_with_children.find_node_by_name("description").node_value == "Moscow geodata samples"

    # Support new Aspose.GIS GeoJsonLayer Class for the support of Format-Specific Features and Non-Destructive Edit
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-54
    # https://issue.saltov.dynabic.com/issues/GISNET-1941
    def GISNET1941Test(self):
        input_path = self.GetFileInBaseFolder("custom_field.json")
        source_path = AbstractPath.from_local_path(input_path)

        with Drivers.geo_json.open_as_geo_json_layer(source_path, GeoJsonOptions()) as l:
            layer = cast(GeoJsonLayer, l)
            assert layer.attributes.count == 1