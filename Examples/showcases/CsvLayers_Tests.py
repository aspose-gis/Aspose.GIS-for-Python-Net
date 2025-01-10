import os
from datetime import datetime

import pytest
from aspose.gis import VectorLayer, Drivers, ConversionOptions, PointFormats, GeoConvert, GisException, PrecisionModel, \
    NumericFormat, Feature, Dataset, FeatureAttribute, AttributeDataType
from aspose.gis.formats.csv import CsvOptions
from aspose.gis.formats.filegdb import FileGdbOptions
from aspose.gis.formats.geojson import GeoJsonOptions
from aspose.gis.formats.shapefile import ShapefileOptions
from aspose.gis.formats.topojson import TopoJsonOptions
from aspose.gis.geometries import IPoint, ILineString, Geometry, Point, LineString, GeometryCollection, CircularString, \
    CompoundCurve, ICircularString, CurvePolygon, MultiCurve, MultiLineString, MultiPoint, LinearRing, Polygon, \
    MultiPolygon, MultiSurface, GeometryType, WkbVariant, WktVariant
from aspose.gis.spatialreferencing import SpatialReferenceSystem, ProjectedSpatialReferenceSystemParameters, Unit, \
    AxisDirection, ProjectedAxisesOrder, Identifier, Axis
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.FolderSettings import FolderSettings
from utils.LicenseHelper import LicenseHelper
class CsvLayers_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    def ReadCsvFeaturesTest(self):
        input = os.path.join(FolderSettings.CommonTestFolder(), "sample.csv")

        with Drivers.csv.open_layer(input) as layer:
            # print attributes
            result = ""
            for attribute in layer.attributes:
                print(f"'{attribute.name}' ", end='')
                result = result + attribute.name + " ";
            print()

            assert result.strip() == "Id City Counter"

            # print records
            result = "";
            for feature in layer:
                dump = feature.get_values_dump(None)
                for item in dump:
                    print(f"'{item}' ", end='')
                    result = result + item + " "
                print()
            assert result.strip() == "1 London 25 2 Paris 35"

    def ReadCsvPointsTest(self):
        input = os.path.join(FolderSettings.CommonTestFolder(), "geometries.csv")

        result = ""
        opt = CsvOptions()
        opt.column_wkt = "geom_data"
        with Drivers.csv.open_layer(input, opt) as layer:
            for feature in layer:
                result = result + feature.geometry.as_text() + " "

        print(result)
        assert result.strip() == "LINESTRING (0 0, 1 1) LINESTRING (10 10, 5 5)"

    def WriteCsvFeaturesTest(self):
        # apply a custom delimiter and a column for geometry.
        options = CsvOptions()
        options.column_wkt = "geom_data"
        options.delimiter = ";"

        input = os.path.join(FolderSettings.BaseTestOutputFolder(), "csv_out.csv")
        # create a new CSV layer
        with Drivers.csv.create_layer(input, options) as layer:
            layer.attributes.add(FeatureAttribute("string_data", AttributeDataType.STRING))
            layer.attributes.add(FeatureAttribute("int_data", AttributeDataType.INTEGER))
            layer.attributes.add(FeatureAttribute("bool_data", AttributeDataType.BOOLEAN))
            layer.attributes.add(FeatureAttribute("float_data", AttributeDataType.DOUBLE))

            feature = layer.construct_feature()
            feature.set_value("string_data", "string value")
            feature.set_value("int_data", 10)
            feature.set_value("bool_data", True)
            feature.set_value("float_data", 3.14)
            feature.geometry = LineString([Point(0, 0), Point(1, 1)])

            layer.add(feature)

            feature2 = layer.construct_feature()
            feature2.set_value("string_data", "string value2")
            feature2.set_value("int_data", 100)
            feature2.set_value("bool_data", False)
            feature2.set_value("float_data", 3.1415)
            feature2.geometry = Geometry.null

            layer.add(feature2)
        print(str(feature))
        out1 = ', '.join([str(x) for x in feature.get_values_dump(None)])
        out2 = ', '.join([str(x) for x in feature2.get_values_dump(None)])
        print(out1)
        assert out1 == "string value, 10, True, 3.14"
        print(out2)
        assert out2 == "string value2, 100, False, 3.1415"

