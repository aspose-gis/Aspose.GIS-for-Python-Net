import pytest
from aspose.gis import Drivers, VectorLayer, Driver, Extent, Dataset
from aspose.gis.formats.filegdb import FileGdbOptions

from aspose.gis.geometries import Point, GeometryType, LineString, LinearRing, Polygon
from aspose.gis.geotools import GeneratorTiles, GeneratorTilesRenderOptions
from aspose.gis.spatialreferencing import SpatialReferenceSystem

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

class Release_25_07_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Support Reading Kmz Format
    # https://issue.saltov.dynabic.com/issues/GISNET-1868
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-34
    def GISNET1868Test(self):
        open_path = self.GetFileInOutputFolder("newfile.gdb")

        # Create FileGDB options
        opt = FileGdbOptions()
        opt.has_m = False
        opt.has_z = False
        opt.expected_geometry_type = GeometryType.POINT

        # Create dataset and layer
        with Drivers.file_gdb.create_dataset(open_path) as dataset:
            with dataset.create_layer("empty_layer", opt, SpatialReferenceSystem.wgs84) as vector_layer:
                pass  # Layer operations would go here

        # Verify the created dataset
        with Dataset.open(open_path, Drivers.file_gdb) as dataset:
            assert dataset.layers_count == 1
            assert dataset.open_layer_at(0, None).geometry_type == GeometryType.POINT