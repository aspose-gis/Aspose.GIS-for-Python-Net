import os
from datetime import datetime
from io import BytesIO

import pytest
from aspose.gis import VectorLayer, Drivers, ConversionOptions, PointFormats, GeoConvert, GisException, PrecisionModel, \
    NumericFormat, Feature, Dataset, FeatureAttribute, AttributeDataType, AbstractPath
from aspose.gis.formats.csv import CsvOptions
from aspose.gis.formats.filegdb import FileGdbOptions
from aspose.gis.formats.geojson import GeoJsonOptions
from aspose.gis.formats.gml import GmlOptions
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
class ReadFeatures_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    def ReadGMLWithoutSpecifyingGMLOptionsTest(self):
        input = os.path.join(FolderSettings.CommonTestFolder(), "file.gml")
        # Case 1: Load schema from the Internet
        options = GmlOptions()
        options.schema_location = None  # Keeping it null to let Aspose.GIS read from the XML file
        options.load_schemas_from_internet = True # Allow loading schemas from the Internet

        print("from internet loading...")
        with VectorLayer.open(input, Drivers.gml, options) as layer:
            i = 0
            for feature in layer:
                i += 1
                print(feature.get_value("attribute"))
                assert feature.get_value("attribute") == f"value{i}"

        # Case 2: Restore the attributes schema by data in the file
        print("")
        print("restoration by file data...")

        gmlRestoreOpt = GmlOptions()
        gmlRestoreOpt.restore_schema = True
        with VectorLayer.open(input, Drivers.gml, gmlRestoreOpt) as layer:
            i = 0
            for feature in layer:
                i += 1
                print(feature.get_value("attribute"))
                assert feature.get_value("attribute") == f"value{i}"

    def ReadGMLBySpecifyingGMLOptionsTest(self):
        # Specify custom schema location since there is no 'schemaLocation' in the GML file
        options = GmlOptions()
        options.schema_location = "http://www.aspose.com  schema.xsd"  # Custom schema location
        options.load_schemas_from_internet = False  # Do not load schemas from the Internet

        print("")
        print("custom schema location...")
        with VectorLayer.open(
                os.path.join(FolderSettings.CommonTestFolder(), "file_without_schema_location.gml"),
                Drivers.gml,
                options) as layer:
            i = 0
            for feature in layer:
                i += 1
                print(feature.get_value("attribute"))
                assert feature.get_value("attribute") == f"value{i}"

    def ReadFeaturesFromMapInfoInterchangeTest(self):
        input = os.path.join(FolderSettings.CommonTestFolder(), "data.mif")
        reference = os.path.join(FolderSettings.CommonTestFolder(), "data.mif.ref.txt")

        with Drivers.map_info_interchange.open_layer(input) as layer:
            res = f"Number of features is {layer.count}.\n"

            last_geometry = layer[layer.count - 1].geometry
            res += f"Last geometry is {last_geometry.as_text()}.\n"

            for feature in layer:
                res += feature.geometry.as_text() + "\n"

        print(res)

        assert res.strip() == Comparison.read_file(reference)

    def ReadFeaturesFromMapInfoTabTest(self):
        input = os.path.join(FolderSettings.CommonTestFolder(), "data.tab")
        reference = os.path.join(FolderSettings.CommonTestFolder(), "data.tab.ref.txt")

        with Drivers.map_info_tab.open_layer(input) as layer:
            res = f"Number of features is {layer.count}.\n"

            last_geometry = layer[layer.count - 1].geometry
            res += f"Last geometry is {last_geometry.as_text()}.\n"

            for feature in layer:
                res += feature.geometry.as_text() + "\n"

        print(res)

        assert res.strip() == Comparison.read_file(reference)

    def ReadFeaturesFromOSMXMLTest(self):
        input = os.path.join(FolderSettings.CommonTestFolder(), "fountain.osm")
        reference = os.path.join(FolderSettings.CommonTestFolder(), "data.osm.ref.txt")
        with Drivers.osm_xml.open_layer(input) as layer:
            # Get features count
            count = layer.count

            print(f"Layer count: {count}")
            assert count == 7

            # Get feature at index 2
            feature_at_index_2 = layer[2]

            res = ""
            # Iterate through all features
            for feature in layer:
                # Handle feature
                res += feature.geometry.as_text()

        print(res)

        assert res.strip() == Comparison.read_file(reference)

    def ReadGeoJsonFromStreamTest(self):
        geo_json = '''{
            "type": "FeatureCollection",
            "features": [
                {"type": "Feature", "geometry": {"type": "Point", "coordinates": [0, 1]}, "properties": {"name": "John"}},
                {"type": "Feature", "geometry": {"type": "Point", "coordinates": [2, 3]}, "properties": {"name": "Mary"}}
            ]
        }'''

        # Use a BytesIO stream to simulate a memory stream
        with BytesIO(geo_json.encode('utf-8')) as memory_stream:
            with Drivers.geo_json.open_layer(AbstractPath.from_stream(memory_stream)) as layer:
                print(layer.count)  # 2
                assert layer.count == 2
                print(layer[1].get_value("name"))  # Mary
                assert layer[1].get_value("name") == "Mary"