import hashlib
import math
from os import path

import pytest
from aspose.gis import Drivers, VectorLayer, Driver, Extent, Dataset, AbstractPath, DynamicFeature, NodeLink, \
    FeatureAttribute, AttributeDataType
from aspose.gis.formats.filegdb import FileGdbOptions
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
class Release_25_11_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Support of the Write Layer for GeoPackage (for raster tile image)
    # https://issue.saltov.dynabic.com/issues/GISNET-1906
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-51
    def GISNET1906Test(self):
        test_path = self.GetFileInOutputFolder("CombineRasterAndVectorLayers.gpkg")
        test_tile_path = self.GetFileInBaseFolder("9-140-292.png")
        reference_path = self.GetFileInBaseFolder("CombineRasterAndVectorLayers.gpkg")

        # Create geometry from WKT
        geometry = Geometry.from_text("POLYGON((10 20,10 40,30 40,30 20,10 20))",
                                      SpatialReferenceSystem.wgs84)

        # Create tile matrix set and options
        tile_matrix_set = GeoPackageTileMatrixSet(-20037508.3427892, -20037508.3427892, 0, 0)
        options = GeoPackageTileOptions(tile_matrix_set)

        # Create dataset and layers
        with Dataset.create(AbstractPath.from_local_path(test_path), Drivers.geo_package) as new_dataset:
            dataset = cast(GeoPackageDataset, new_dataset)
            # Create vector layer
            new_layer = dataset.create_layer("Layer_1", SpatialReferenceSystem.wgs84)
            feature = new_layer.construct_feature()
            feature.geometry = geometry
            new_layer.add(feature)

            # Create tile layer
            dataset.create_tile_layer("tile_1", test_tile_path, options, SpatialReferenceSystem.wgs84)

        Comparison.compare_binary_files(reference_path, test_path)


    # Support of Spatial Reference System editing in GeoPackage (GPKG)
    # https://issue.saltov.dynabic.com/issues/GISNET-1922
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-52
    def GISNET1922Test(self):
        test_path = self.GetFileInOutputFolder("WriteTwoLayersAndTwoFeatures.gpkg")
        reference_path = self.GetFileInBaseFolder("WriteTwoLayersAndTwoFeatures.gpkg")

        # For example:
        geometry_1 = Geometry.from_text("POINT(10 20)", SpatialReferenceSystem.wgs84)
        geometry_2 = Geometry.from_text("POINT(30 40)", SpatialReferenceSystem.wgs84)

        with Dataset.create(test_path, Drivers.geo_package) as new_dataset:
            # Create layer with WGS84 spatial reference
            new_layer = new_dataset.create_layer("Layer_1", SpatialReferenceSystem.wgs84)

            # Create and add first feature
            feature_1 = new_layer.construct_feature()
            feature_1.geometry = geometry_1  # Make sure geometry_1 is defined
            new_layer.add(feature_1)

            # Create and add second feature
            feature_2 = new_layer.construct_feature()
            feature_2.geometry = geometry_2  # Make sure geometry_2 is defined
            new_layer.add(feature_2)

        Comparison.compare_binary_files(reference_path, test_path)

#LicenseHelper.set_license()
#tests = Release_25_11_Tests()
#tests.GISNET1922Test()