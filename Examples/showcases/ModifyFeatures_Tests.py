import os
from datetime import datetime

import pytest
from aspose.gis import VectorLayer, Drivers, ConversionOptions, PointFormats, GeoConvert, GisException, PrecisionModel, \
    NumericFormat, Feature, Dataset, FeatureAttribute, AttributeDataType
from aspose.gis.formats.shapefile import ShapefileOptions
from aspose.gis.geometries import IPoint, ILineString, Geometry, Point, LineString, GeometryCollection, CircularString, \
    CompoundCurve, ICircularString, CurvePolygon, MultiCurve, MultiLineString, MultiPoint, LinearRing, Polygon, \
    MultiPolygon, MultiSurface, GeometryType, WkbVariant, WktVariant

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.FolderSettings import FolderSettings
from utils.LicenseHelper import LicenseHelper
class ModifyFeatures_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    def AddFeaturesInExistShapeFileTest(self):
        from_path = os.path.join(FolderSettings.CommonTestFolder(), "point_xyz")
        to_path = os.path.join(FolderSettings.BaseTestOutputFolder(), "point_xyz_out")
        reference_folder = os.path.join(FolderSettings.CommonTestFolder(), "point_xyz_ref")

        FolderSettings.copy_folder(from_path, to_path)
        path = os.path.join(to_path, "point_xyz.shp")

        with Drivers.shapefile.edit_layer(path, ShapefileOptions()) as layer:
            feature = layer.construct_feature()
            feature.set_value("ID", 5) # Assuming the method sets a value for the attribute "ID"
            point = Point(-5, 5)
            point.z = 2 # Set Z value for the point
            feature.geometry = point

            layer.add(feature)

        Comparison.compare_folders(to_path, reference_folder)

    def ModifyFeaturesInSingleLayerTest(self):
        source_path = os.path.join(FolderSettings.CommonTestFolder(), "InputShapeFile.shp")

        reference_folder = os.path.join(FolderSettings.CommonTestFolder(), "single_layer_modify")
        result_folder = os.path.join(FolderSettings.BaseTestOutputFolder(), "single_layer_modify")
        result_path = os.path.join(result_folder, "modified_out.shp")

        if not os.path.exists(result_folder):
            os.makedirs(result_folder)

        with VectorLayer.open(source_path, Drivers.shapefile) as source:
            with VectorLayer.create(result_path, Drivers.shapefile, source.spatial_reference_system) as result:
                result.copy_attributes(source)

                for feature in source:
                    # Modify the geometry
                    modified_geometry = feature.geometry.get_buffer(2.0, 30)
                    feature.geometry = modified_geometry

                    # Modify a feature attribute
                    attribute_value = feature.get_value("name")
                    modified_attribute_value = attribute_value.upper()
                    feature.set_value("name", modified_attribute_value)

                    result.add(feature)

        Comparison.compare_folders(result_folder, reference_folder)

    def ModifyFeaturesInDatasetTest(self):
        source_path = os.path.join(FolderSettings.CommonTestFolder(), "InputShapeFile.shp")
        result_folder = os.path.join(FolderSettings.BaseTestOutputFolder(), "dataset_modify")
        result_path = os.path.join(result_folder, "modified_out.shp")
        if not os.path.exists(result_folder):
            os.makedirs(result_folder)

        reference_folder = os.path.join(FolderSettings.CommonTestFolder(), "dataset_modify")

        with VectorLayer.open(source_path, Drivers.shapefile) as source:
            with VectorLayer.create(result_path, Drivers.shapefile, source.spatial_reference_system) as result:
                result.copy_attributes(source)

                for feature in source:
                    # Modify the geometry
                    modified_geometry = feature.geometry.get_buffer(2.0, 30)
                    feature.geometry = modified_geometry

                    # Modify a feature attribute
                    attribute_value = feature.get_value("name")
                    modified_attribute_value = attribute_value.upper()
                    feature.set_value("name", modified_attribute_value)

                    result.add(feature)

        Comparison.compare_folders(result_folder, reference_folder)