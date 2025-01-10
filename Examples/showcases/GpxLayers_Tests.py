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
from aspose.gis.spatialreferencing import SpatialReferenceSystem, ProjectedSpatialReferenceSystemParameters, Unit, \
    AxisDirection, ProjectedAxisesOrder, Identifier, Axis
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.FolderSettings import FolderSettings
from utils.LicenseHelper import LicenseHelper
class GpxLayers_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    def ReadGPXFeaturesTest(self):
        input = os.path.join(FolderSettings.CommonTestFolder(), "schiehallion.gpx")
        reference = os.path.join(FolderSettings.CommonTestFolder(), "schiehallion_ref.txt")
        res = ""
        with Drivers.gpx.open_layer(input) as layer:
            for feature in layer:
                geometry_type = feature.geometry.geometry_type
                # GPX waypoints are exported as features with point geometry.
                if geometry_type == GeometryType.POINT:
                    print(feature.geometry.dimension)
                    res += " " + str(feature.geometry.dimension)
                    # HandleGpxWaypoint(feature)

                # GPX routes are exported as features with line string geometry.
                elif geometry_type == GeometryType.LINE_STRING:
                    # HandleGpxRoute(feature)
                    ls = feature.geometry  # Assuming feature.geometry is already a LineString type
                    for point in ls:
                        print(point.as_text())
                        res += " " + point.as_text()

                # GPX tracks are exported as features with multi line string geometry.
                # Every track segment is a line string.
                elif geometry_type == GeometryType.MULTI_LINE_STRING:
                    # HandleGpxTrack(feature)
                    print(feature.geometry.as_text())
                    res += " " + feature.geometry.as_text()

                else:
                    pass  # Handle other geometry types if necessary

        assert res.strip() == Comparison.read_file(reference)

    def ReadGPXNestedAttributesTest(self):
        # Specify option
        options = GpxOptions()
        options.read_nested_attributes = True
        input = os.path.join(FolderSettings.CommonTestFolder(), "nested_data.gpx")
        reference = os.path.join(FolderSettings.CommonTestFolder(), "nested_data_ref.txt")

        res = ""
        # Open GPX layer to read features
        with Drivers.gpx.open_layer(input, options) as layer:
            for feature in layer:
                if feature.geometry.geometry_type == GeometryType.MULTI_LINE_STRING:
                    # Read segment
                    lines = feature.geometry
                    for i in range(lines.count):

                        print(f"....segment({i})......")
                        res +=f"....segment({i})......";
                        segment = lines[i]

                        # Read points in segment
                        for j in range(len(segment)):
                            # Look for attribute
                            attribute_name = f"name__{i}__{j}"

                            names = [x.name for x in layer.attributes]
                            if (attribute_name in names and feature.is_value_set(attribute_name)):
                                # Print a point and attribute
                                value = feature.get_value(attribute_name)
                                print(f"{segment[j].as_text()} - {attribute_name}: {value}, ")
                                res += f"{segment[j].as_text()} - {attribute_name}: {value}, ";
                            else:
                                # Print a point only
                                print(segment[j].as_text())
                                res += segment[j].as_text()
                    print("..........")
                    res += ".........."

                    assert res == Comparison.read_file(reference)

    def WriteGpxPolygonsAsLinesTest(self):
        # Adjust based on your actual method for getting data directory
        gpx_output_path = os.path.join(FolderSettings.BaseTestOutputFolder(), "lines_out.gpx")
        gpx_reference =  os.path.join(FolderSettings.CommonTestFolder(), "lines_ref.gpx")

        opt = GpxOptions()
        opt.write_polygons_as_lines = True
        # Create a layer with options to write polygons as lines
        with Drivers.gpx.create_layer(gpx_output_path, opt) as layer:
            # The GPX format does not support polygons,
            # but we use the WritePolygonsAsLines option to resolve this issue.
            feature = layer.construct_feature()
            feature.geometry = Geometry.from_text("POLYGON((1 2, 1 4, 3 4, 3 2))")
            layer.add(feature)

        Comparison.compare_binary_files(gpx_output_path, gpx_reference)

    # Input data doesn't contain values for calculations. Was Checked in .NET Version
    def CalculateAverageSpeedOfRouteTest(self):
        gpx_file_path = os.path.join(FolderSettings.CommonTestFolder(), "schiehallion.gpx")

        options = GpxOptions()
        # Set MAttribute to "speed"
        options.m_attribute = "speed"

        with Drivers.gpx.open_layer(gpx_file_path) as layer:
            route_feature = None

            # Find the route feature with GeometryType LineString
            for feature in layer:  # Assuming layer has a features attribute
                if feature.geometry.geometry_type == GeometryType.LINE_STRING:
                    route_feature = feature
                    break

            if route_feature is not None:
                route_geometry = route_feature.geometry  # Assuming this returns an ILineString-like object
                points_with_speed = []

                # Filter out points without "speed"
                for point in route_geometry:
                    if point.has_m:  # Assuming point has a has_m property
                        points_with_speed.append(point)

                # Calculate the average speed
                total_speed = 0
                count = 0

                for point in points_with_speed:
                    total_speed += point.m  # Assuming point has an m property
                    count += 1

                average_speed = total_speed / count if count > 0 else 0
                print("Average Speed: " + str(average_speed))
                assert average_speed == 0
            else:
                raise "Layer not found"