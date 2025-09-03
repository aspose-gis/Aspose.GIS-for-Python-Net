import os
from uuid import UUID

import pytest
from aspose.gis import Drivers, VectorLayer, FeatureAttribute, AttributeDataType, GeoConvert, \
    PointFormats

from aspose.gis.formats.mapinfointerchange import MapInfoInterchangeOptions
from aspose.gis.spatialreferencing import SpatialReferenceSystem
from datetime import datetime, time
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

class Release_25_03_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Write data to MapInfoInterchange Format
    # https://issue.saltov.dynabic.com/issues/GISNET-1794
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-14
    def GISNET1794Test(self):

        file_path = self.GetFileInOutputFolder("mapinfo.mif")
        ref_path = self.GetFileInBaseFolder("mapinfo.mif")

        options = MapInfoInterchangeOptions()
        spatial_reference_system = SpatialReferenceSystem.wgs84

        with Drivers.map_info_interchange.create_layer(file_path, options, spatial_reference_system) as layer:
            layer.attributes.add(FeatureAttribute("Integer", AttributeDataType.INTEGER))
            layer.attributes.add(FeatureAttribute("Long", AttributeDataType.LONG))
            layer.attributes.add(FeatureAttribute("Boolean", AttributeDataType.BOOLEAN))
            layer.attributes.add(FeatureAttribute("Double", AttributeDataType.DOUBLE))
            layer.attributes.add(FeatureAttribute("Date", AttributeDataType.DATE))
            layer.attributes.add(FeatureAttribute("DateTime", AttributeDataType.DATE_TIME))
            layer.attributes.add(FeatureAttribute("Time", AttributeDataType.TIME))
            layer.attributes.add(FeatureAttribute("String", AttributeDataType.STRING))
            layer.attributes.add(FeatureAttribute("Guid", AttributeDataType.GUID))

            feature = layer.construct_feature()
            feature.set_value("Integer", 1234)
            feature.set_value("Long", 4321)
            feature.set_value("Boolean", False)
            feature.set_value("Double", 3.14)
            feature.set_value("Date", datetime(2017, 8, 24))
            feature.set_value("DateTime", datetime(2017, 8, 24, 14, 12, 33))
            feature.set_value("Time", time(14, 12, 33))
            feature.set_value("String", "Hello")
            feature.set_value("Guid", UUID('00000001-0002-0003-0004-000506070809'))

            layer.add(feature)

        Comparison.compare_binary_files(file_path, ref_path)

    # Support UTM and UPS Formats
    # https://issue.saltov.dynabic.com/issues/GISNET-1779
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-15
    def GISNET1779Test(self):
        # UTM Conversion
        point_text = GeoConvert.as_point_text(25.5, 45.5, PointFormats.UTM)
        if point_text != "38R 550249mE 2820408mN":
            raise Exception("Conversion was incorrect")

        # X is longitude and Y is latitude
        point_parse = GeoConvert.parse_point_text("56X;461235mE;8882252mN")
        if abs(point_parse.x - 151) > 0.0001 or abs(point_parse.y - 80) > 0.0001:
            raise Exception("Conversion was incorrect")

        # UPS Conversion
        # Note: Should this be PointFormats.UPS?
        point_text = GeoConvert.as_point_text(81, 151, PointFormats.UTM)
        if point_text != "56X 465078mE 8993806mN":
            raise Exception("Conversion was incorrect")

        point_parse = GeoConvert.parse_point_text("A 1730708mE 1514186mN")
        if abs(point_parse.x + 151) > 0.0001 or abs(point_parse.y + 85) > 0.0001:
            raise Exception("Conversion was incorrect")