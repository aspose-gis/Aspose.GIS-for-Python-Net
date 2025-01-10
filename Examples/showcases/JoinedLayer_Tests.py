import os
from datetime import datetime

import pytest
from aspose.gis import VectorLayer, Drivers, ConversionOptions, PointFormats, GeoConvert, GisException, PrecisionModel, \
    NumericFormat, Feature, Dataset, FeatureAttribute, AttributeDataType
from aspose.gis.formats.csv import CsvOptions
from aspose.gis.formats.filegdb import FileGdbOptions
from aspose.gis.formats.geojson import GeoJsonOptions
from aspose.gis.formats.gpx import GpxOptions
from aspose.gis.formats.shapefile import ShapefileOptions
from aspose.gis.formats.topojson import TopoJsonOptions
from aspose.gis.geometries import IPoint, ILineString, Geometry, Point, LineString, GeometryCollection, CircularString, \
    CompoundCurve, ICircularString, CurvePolygon, MultiCurve, MultiLineString, MultiPoint, LinearRing, Polygon, \
    MultiPolygon, MultiSurface, GeometryType, WkbVariant, WktVariant
from aspose.gis.relationship.joins import JoinOptions
from aspose.gis.spatialreferencing import SpatialReferenceSystem, ProjectedSpatialReferenceSystemParameters, Unit, \
    AxisDirection, ProjectedAxisesOrder, Identifier, Axis
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.FolderSettings import FolderSettings
from utils.LicenseHelper import LicenseHelper


class JoinedLayer_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    def JoinByNameTest(self):
        input1 = os.path.join(FolderSettings.CommonTestFolder(), "main.kml")
        input2 = os.path.join(FolderSettings.CommonTestFolder(), "second.kml")

        # one-to-one left join two layers by 'city' attribute
        options = JoinOptions()
        options.join_attribute_name = "city"
        options.target_attribute_name = "city"

        with Drivers.kml.open_layer(input1) as main:
            with Drivers.kml.open_layer(input2) as second:
                with main.join(second, options) as joined:
                    # read and print joined
                    features_count = joined.count
                    attributes_count = joined.attributes.count
                    spatial_ref_sys = joined.spatial_reference_system
                    code = spatial_ref_sys.epsg_code if spatial_ref_sys is not None else "'no srs'"
                    joined_temp_value = joined[0].get_value("joined_temp")

                    print(f"featuresCount: {features_count}")
                    assert features_count == 10
                    print(f"attributesCount: {attributes_count}")
                    assert attributes_count == 20
                    print(f"spatialRefSys: {code}")
                    assert code == "'no srs'"
                    print(f"joinedTempValue: {joined_temp_value}")
                    assert joined_temp_value == 32

    def JoinWithConditionComparerTest(self):
        # At this moment custom comparers are not supported in Python version
        pass
        # # One-to-one left join two layers by 'city' attribute
        # options = JoinOptions()
        # options.join_attribute_name = "city"
        # options.target_attribute_name = "city"
        #
        # # Use custom comparer
        # options.condition_comparer = InsensitiveComparer()
        #
        # input1 = os.path.join(FolderSettings.CommonTestFolder(), "main.kml")
        # input2 = os.path.join(FolderSettings.CommonTestFolder(), "second.kml")
        #
        # with Drivers.kml.open_layer(input1) as main:
        #     with Drivers.kml.open_layer(input2) as second:
        #         with main.join(second, options) as joined:
        #             # Read and print joined
        #             features_count = joined.count
        #             attributes_count = joined.attributes.count
        #             spatial_ref_sys = joined.spatial_reference_system
        #             code = spatial_ref_sys.epsg_code if spatial_ref_sys is not None else "'no srs'"
        #             city_value = joined[4].get_value("city")
        #             joined_city_value = joined[4].get_value("joined_city")
        #
        #             print(f"featuresCount: {features_count}")
        #             print(f"attributesCount: {attributes_count}")
        #             print(f"spatialRefSys: {code}")
        #             print(f"cityValue: {city_value}")
        #             print(f"joinedCityValue: {joined_city_value}")

    def JoinFewAttributesTests(self):
        # One-to-one left join two layers by 'city' attribute
        options = JoinOptions()
        options.join_attribute_name = "city"
        options.target_attribute_name = "city"

        # Define attributes to join
        options.join_attribute_names = ["temp", "date"]

        input1 = os.path.join(FolderSettings.CommonTestFolder(), "main.kml")
        input2 = os.path.join(FolderSettings.CommonTestFolder(), "second.kml")

        with Drivers.kml.open_layer(input1) as main:
            with Drivers.kml.open_layer(input2) as second:
                with main.join(second, options) as joined:
                    # Read and print joined
                    features_count = joined.count
                    attributes_count = joined.attributes.count
                    spatial_ref_sys = joined.spatial_reference_system
                    code = spatial_ref_sys.epsg_code if spatial_ref_sys is not None else "'no srs'"

                    print(f"featuresCount: {features_count}")
                    assert features_count == 10
                    print(f"attributesCount: {attributes_count}")
                    assert attributes_count == 12
                    print(f"spatialRefSys: {code}")
                    assert code == "'no srs'"