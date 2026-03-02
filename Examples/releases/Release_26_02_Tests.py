import os

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

class Release_26_02_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Exception on conversion of KMZ format in a Loop
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-63
    # https://issue.saltov.dynabic.com/issues/GISNET-1955
    def GISNET1955Test(self):
        open_path = self.GetFileInBaseFolder("doc_kmz.kmz")
        # Check in loop of bug from forum
        for i in range(2):
            with Drivers.kml.open_layer(open_path) as layer:
                feature1 = layer[0]
                assert feature1.get_value("name") == "G74"

                feature2 = layer[1]
                assert feature2.get_value("name") == "G73"

                assert layer.geometry_type == GeometryType.POINT
                assert layer.count == 115

                # Check KmlFeaturesEnumerator
                for f in layer:
                    pass

    # Exception during Conversion GeoJsonSeq to Csv
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-64
    # https://issue.saltov.dynabic.com/issues/GISNET-1956
    def GISNET1956Test(self):
        # Out of range latitude test
        source_path = self.GetFileInBaseFolder("geojsonseq.json")
        destination_path = self.GetFileInOutputFolder("output.csv")
        VectorLayer.convert(source_path, Drivers.geo_json_seq, destination_path, Drivers.csv)

        with VectorLayer.open(destination_path, Drivers.csv) as layer:
            assert layer.count == 3
            assert layer.attributes.count == 2

    # Improving of GPX format exceptions details
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-68
    # https://issue.saltov.dynabic.com/issues/GISNET-1967
    def GISNET1967Test(self):
        source_path = self.GetFileInBaseFolder("polygon.shp")
        destination_path = self.GetFileInOutputFolder("output.gpx")

        with pytest.raises(Exception) as exc_info:
            VectorLayer.convert(source_path, Drivers.shapefile, destination_path, Drivers.gpx)

        # Check Exception text
        assert exc_info.type.__name__ == "RuntimeError"
        assert str(exc_info.value) == "Proxy error(InvalidOperationException): The GpxDriver does not support Polygon geometry type"

LicenseHelper.set_license()
tests = Release_26_02_Tests()
tests.GISNET1967Test()