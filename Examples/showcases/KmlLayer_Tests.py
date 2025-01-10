import os
from datetime import datetime

import pytest
from aspose.gis import VectorLayer, Drivers, ConversionOptions, PointFormats, GeoConvert, GisException, PrecisionModel, \
    NumericFormat, Feature, Dataset, FeatureAttribute, AttributeDataType
from aspose.gis.formats.csv import CsvOptions
from aspose.gis.formats.filegdb import FileGdbOptions
from aspose.gis.formats.geojson import GeoJsonOptions
from aspose.gis.formats.gpx import GpxOptions
from aspose.gis.formats.kml import KmlOptions
from aspose.gis.formats.kml.styles import KmlFeatureStyle, KmlLineStyle, KmlPolygonStyle, KmlIconStyle, KmlIconResource, \
    KmlLabelStyle, KmlBalloonStyle, KmlListStyle, KmlItemTypes
from aspose.gis.formats.shapefile import ShapefileOptions
from aspose.gis.formats.topojson import TopoJsonOptions
from aspose.gis.geometries import IPoint, ILineString, Geometry, Point, LineString, GeometryCollection, CircularString, \
    CompoundCurve, ICircularString, CurvePolygon, MultiCurve, MultiLineString, MultiPoint, LinearRing, Polygon, \
    MultiPolygon, MultiSurface, GeometryType, WkbVariant, WktVariant
from aspose.gis.relationship.joins import JoinOptions
from aspose.gis.spatialreferencing import SpatialReferenceSystem, ProjectedSpatialReferenceSystemParameters, Unit, \
    AxisDirection, ProjectedAxisesOrder, Identifier, Axis
from aspose.pycore import cast
from aspose.pydrawing import Color

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.FolderSettings import FolderSettings
from utils.LicenseHelper import LicenseHelper
class KmlLayer_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    def CreateKmlFileTest(self):
        output_file_path = os.path.join(FolderSettings.BaseTestOutputFolder(), "Kml_File_out.kml")
        reference_file_path = os.path.join(FolderSettings.CommonTestFolder(), "Ref_Kml_File_out.kml")

        with Drivers.kml.create_layer(output_file_path) as layer:
            layer.attributes.add(FeatureAttribute("string_data", AttributeDataType.STRING))
            layer.attributes.add(FeatureAttribute("int_data", AttributeDataType.INTEGER))
            layer.attributes.add(FeatureAttribute("bool_data", AttributeDataType.BOOLEAN))
            layer.attributes.add(FeatureAttribute("float_data", AttributeDataType.DOUBLE))

            feature = layer.construct_feature()
            feature.set_value("string_data", "string value")
            feature.set_value("int_data", 10)
            feature.set_value("bool_data", True)
            feature.set_value("float_data", 3.14)
            geometry = LineString()
            geometry.add_point(0, 0)
            geometry.add_point(1, 1)

            feature.geometry = geometry

            layer.add(feature)

            feature2 = layer.construct_feature()
            feature2.set_value("string_data", "string value2")
            feature2.set_value("int_data", 100)
            feature2.set_value("bool_data", False)
            feature2.set_value("float_data", 3.1415)
            feature2.geometry = Geometry.null

            layer.add(feature2)

        Comparison.compare_binary_files(output_file_path, reference_file_path)

    def ReadFeaturesFromKmlTest(self):
        with Drivers.kml.open_layer(os.path.join(FolderSettings.CommonTestFolder(), "kml_file.kml")) as layer:
            # Get features count
            count = layer.count

            feature_at_index_1 = layer[0]
            print(feature_at_index_1.get_value("string_data"))
            assert feature_at_index_1.get_value("string_data") == "string value"

            feature_at_index_2 = layer[1]
            print(feature_at_index_2.get_value("string_data"))
            assert feature_at_index_2.get_value("string_data") == "string value2"

    def ReadFeaturesFromInvalidKmlTest(self):
        path = os.path.join(FolderSettings.CommonTestFolder(), "kml_invalid_chars.kml")
        kml_options = KmlOptions()
        kml_options.symbol_to_replace_invalid_chars = '_'

        res = ""
        with Drivers.kml.open_layer(path, kml_options) as layer:
            for feature in layer:
                print(feature.get_value("name"))
                res += feature.get_value("name") + " "
                print(feature.get_value("description"))
                res += feature.get_value("description") + " "

        print(res.strip())
        assert res.strip() == "Vertical_Tab0 End_of_Text0 Vertical_Tab1 End_of_Text1"

    def ExportStylePropertiesToKmlTest(self):
        output_file_path = os.path.join(FolderSettings.BaseTestOutputFolder(), "Kml_Styles_out.kml")
        reference_file_path = os.path.join(FolderSettings.CommonTestFolder(), "Ref_Kml_Styles_out.kml")

        with Drivers.kml.create_layer(output_file_path) as layer:
            style = KmlFeatureStyle()
            style.line = KmlLineStyle()
            style.line.width = width=2.0

            style.polygon = KmlPolygonStyle()
            style.polygon.outline = False
            style.icon = KmlIconStyle()
            style.icon.resource = KmlIconResource()
            style.icon.resource.href = "url"
            style.label = KmlLabelStyle()
            style.label.color = Color.green
            style.balloon = KmlBalloonStyle()
            style.balloon.background_color = Color.aqua
            style.balloon.text = "Example"
            style.list = KmlListStyle()
            style.list.item_type = KmlItemTypes.RADIO_FOLDER

            feature = layer.construct_feature()
            geom = LineString()
            geom.add_point(0, 0)
            geom.add_point(1, 1)
            feature.geometry = geom

            layer.add(feature, style)

            feature2 = layer.construct_feature()
            feature2.geometry = Point(5, 5)

            layer.add(feature2, style)

        Comparison.compare_binary_files(output_file_path, reference_file_path)