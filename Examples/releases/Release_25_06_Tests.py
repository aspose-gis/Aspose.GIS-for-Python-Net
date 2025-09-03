import pytest
from aspose.gis import Drivers, VectorLayer, Driver, Extent

from aspose.gis.geometries import Point, GeometryType, LineString, LinearRing, Polygon
from aspose.gis.geotools import GeneratorTiles, GeneratorTilesRenderOptions

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

class Release_25_06_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Support Reading Kmz Format
    # https://issue.saltov.dynabic.com/issues/GISNET-1842
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-27
    def GISNET1842Test(self):
        open_path = self.GetFileInBaseFolder("doc_kmz.kmz")

        with Drivers.kml.open_layer(open_path, None) as layer:
            feature1 = layer[0]
            assert feature1.get_value("name") == "G74"

            feature2 = layer[1]
            assert feature2.get_value("name") == "G73"

            assert layer.geometry_type == GeometryType.POINT
            assert layer.count == 115

            # check KmlFeaturesEnumerator
            for feature in layer:
                pass  # do something with each feature

    # Rework And Update Generator Of Tiles
    # https://issue.saltov.dynabic.com/issues/GISNET-1845
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-32
    def GISNET1845Test(self):
        source_path = self.GetFileInBaseFolder("fountain.osm")
        files = ["tile_zxy_1_2,1113359_48,8075886.png", "tile_zxy_1_2,1113359_48,808362475.png", "tile_zxy_1_2,112109775_48,8075886.png", "tile_zxy_1_2,112109775_48,808362475.png"]
        output_folder = self.GetFileInOutputFolder("")
        layer = VectorLayer.open(source_path, Drivers.osm_xml)

        options = GeneratorTilesRenderOptions()
        options.tile_size = 512

        zoom = 1  # You'll need to define the zoom level, as it wasn't specified in the original code

        extent = Extent()
        extent.x_min = 2.1113359
        extent.y_min = 48.8075886
        extent.x_max = 2.11288365
        extent.y_max = 48.80895
        GeneratorTiles.generate_tiles(
            layer,
            output_folder,
            zoom,
            extent,
            options
        )

        for file in files:
            expected = self.GetFileInBaseFolder(file)
            output = self.GetFileInOutputFolder(file)
            Comparison.check_against_ethalon(output, expected, 0)