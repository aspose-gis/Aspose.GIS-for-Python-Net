import os

import pytest
from aspose.gis import Drivers, VectorLayer, FeatureAttribute, AttributeDataType, GeoConvert, \
    PointFormats
import codecs
from aspose.gis.formats.osmxml import OsmXmlOptions
from aspose.gis.formats.shapefile import ShapefileOptions
from aspose.gis.geometries import Point, LinearRing, Polygon, IPoint
from aspose.gis.rendering import Map, Renderers
from aspose.gis.rendering.colorizers import MultiBandColor, BandColor
from aspose.gis.spatialreferencing import SpatialReferenceSystem
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

class Release_25_02_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Support of Maidenhead Format
    # https://issue.saltov.dynabic.com/issues/GISNET-1775
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-12
    def GISNET1775Test(self):
        # Convert coordinates to Maidenhead point text
        point_text = GeoConvert.as_point_text(80.0, 151.0, PointFormats.MAIDENHEAD)

        # Check if the conversion is correct
        if point_text != "QR50ma":
            raise Exception("Conversion was incorrect")

        # Parse Maidenhead point text to coordinates
        point_parse = GeoConvert.parse_point_text("BB40ma")

        # Check if the parsed coordinates are correct
        if (point_parse.x + 151.0) > 0.05 or (point_parse.y + 80.0) > 0.05:
            raise Exception("Conversion was incorrect")

        print("All conversions are correct!")

    # Support of Google Plus Code Format
    # https://issue.saltov.dynabic.com/issues/GISNET-1774
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-11
    def GISNET1774Test(self):
        # Convert coordinates to PlusCode point text
        point_text = GeoConvert.as_point_text(80.0, 151.0, PointFormats.PLUS_CODE)

        # Check if the conversion is correct
        if point_text != "CRGH2222+22":
            raise Exception("Conversion was incorrect")

        # Parse PlusCode point text to coordinates
        point_parse = GeoConvert.parse_point_text("23GF2222+22")

        # Check if the parsed coordinates are correct
        if point_parse.x != -151.0 or point_parse.y != -80.0:
            raise Exception("Conversion was incorrect")

        print("All conversions are correct!")

    # Support of GARS Format
    # https://issue.saltov.dynabic.com/issues/GISNET-1770
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-10
    def GISNET1770Test(self):
        # Convert coordinates to GARS point text
        pointText = GeoConvert.as_point_text(80.0, 151.0, PointFormats.GARS)

        # Check if the conversion is correct
        if (pointText != "663QE37"):
            raise Exception("Conversion was incorrect")

        # Parse GARS point text to coordinates
        pointParse = GeoConvert.parse_point_text("059AW37")

        # Check if the parsed coordinates are correct
        if (pointParse.x != -151.0 or pointParse.y != -80.0):
            raise Exception("Conversion was incorrect")

        print("All conversions are correct!")


