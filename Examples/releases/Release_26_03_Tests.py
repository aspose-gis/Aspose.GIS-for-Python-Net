import os

import pytest
from aspose.gis import Drivers, VectorLayer, Driver, Extent, Dataset, AbstractPath, DynamicFeature, NodeLink, \
    FeatureAttribute, AttributeDataType, ConversionOptions

from aspose.gis.formats.gpx import GpxOptions

from aspose.gis.geometries import Point, GeometryType, LineString, LinearRing, Polygon, Geometry, MultiPolygon

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

class Release_26_03_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Incorrect Count Of Layers For Gpx Format in NET Core 3.1
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-72
    # https://issue.saltov.dynabic.com/issues/GISNET-1984
    def GISNET1984Test(self):
        # Configure conversion options with polygon-to-line transformation
        options = ConversionOptions()
        options.destination_driver_options = GpxOptions()
        options.destination_driver_options.write_polygons_as_lines = True

        source_path = self.GetFileInBaseFolder("daniSample.shp")
        destination_path = self.GetFileInOutputFolder("output.gpx")

        # Convert Shapefile to GPX
        VectorLayer.convert(source_path, Drivers.shapefile, destination_path, Drivers.gpx, options)

        # Verify the conversion results
        with VectorLayer.open(destination_path, Drivers.gpx) as layer:
            assert layer.count == 6
            assert layer.attributes.count == 23

    # Using of "WritePolygonsAsLines" Option For Gpx Format
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-71
    # https://issue.saltov.dynabic.com/issues/GISNET-1976
    def GISNET1976Test(self):
        # Configure conversion options with polygon-to-line transformation
        options = ConversionOptions()
        options.destination_driver_options = GpxOptions()

        # Gpx doesn't support polygons but you can save it in gpx like lines
        options.destination_driver_options.write_polygons_as_lines = True

        source_path = self.GetFileInBaseFolder("daniSample.shp")
        destination_path = self.GetFileInOutputFolder("output.gpx")

        # Convert Shapefile to GPX
        VectorLayer.convert(source_path, Drivers.shapefile, destination_path, Drivers.gpx, options)

        with VectorLayer.open(source_path, Drivers.shapefile) as layer:
            attrCountOriginal = layer.attributes.count

        # Verify the conversion results
        with VectorLayer.open(destination_path, Drivers.gpx) as layer:
            assert layer.attributes.count > attrCountOriginal

    # Support MultiPolygon Geometry Type For EsriJson Format on conversions
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-70
    # https://issue.saltov.dynabic.com/issues/GISNET-1973
    def GISNET1973Test(self):
        # Create a MultiPolygon with two polygons (each with an outer ring and an inner hole)
        multi_polygon = MultiPolygon()

        # First polygon with a hole
        outer_ring1 = LinearRing([
            Point(0, 0), Point(10, 0), Point(10, 10),
            Point(0, 10), Point(0, 0)
        ])
        inner_ring1 = LinearRing([
            Point(3, 3), Point(3, 6), Point(6, 6),
            Point(6, 3), Point(3, 3)
        ])
        polygon1 = Polygon(outer_ring1, [inner_ring1])
        multi_polygon.add(polygon1)

        # Second polygon with a hole
        outer_ring2 = LinearRing([
            Point(30, 0), Point(40, 0), Point(40, 10),
            Point(30, 10), Point(30, 0)
        ])
        inner_ring2 = LinearRing([
            Point(33, 3), Point(33, 6), Point(36, 6),
            Point(36, 3), Point(33, 3)
        ])
        polygon2 = Polygon(outer_ring2, [inner_ring2])
        multi_polygon.add(polygon2)

        outputFile = self.GetFileInOutputFolder("output_esrijson.json")  # Specify your output file path
        referenceFile = self.GetFileInBaseFolder("output_esrijson.json")

        with VectorLayer.create(outputFile, Drivers.esri_json) as layer:
            feature = layer.construct_feature()
            feature.geometry = multi_polygon
            layer.add(feature)

        Comparison.compare_binary_files(outputFile, referenceFile)
        print(f"MultiPolygon successfully written to {outputFile}")