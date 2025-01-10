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
class ReadingESRIFileGeoDatabaseFileGDB_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    def IterateOverLayersInFileGdbTest(self):
        reference = os.path.join(FolderSettings.CommonTestFolder(), "ThreeLayers.dump.ref.txt")
        # File GDB is a multi-layer format. This example shows how to open File GDB as a dataset (collection of layers) and access layers in it.
        with Dataset.open(os.path.join(FolderSettings.CommonTestFolder(), "ThreeLayers.gdb"), Drivers.file_gdb) as dataset:
            assert dataset.layers_count == 3
            res = ""
            for i in range(dataset.layers_count):
                res += f"Layer {i} name: {dataset.get_layer_name(i)} \n"

                with dataset.open_layer_at(i, None) as layer:
                    res += f"Layer has {layer.count} features \n"
                    for feature in layer:
                        res += feature.geometry.as_text() + "\n"
                res += "\n"

            print(res)
            assert res.strip() == Comparison.read_file(reference)