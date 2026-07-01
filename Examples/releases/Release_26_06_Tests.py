import math
import os
import pytest
from aspose.gis import Drivers, VectorLayer, ConversionOptions
from aspose.gis.formats.gml import GmlOptions
from aspose.gis.formats.csv import CsvOptions
from aspose.gis.formats.kml import KmlOptions
from aspose.gis.geometries import LineString, Polygon
from aspose.gis.operations import OperationErrorCollector
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper


class Release_26_06_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Gml To Gml - Results Not The Same In QGIS
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-86
    # https://issue.saltov.dynabic.com/issues/GISNET-2051
    def GISNET2051Test(self):
        options = ConversionOptions()
        sourceGmlOpt = GmlOptions()
        sourceGmlOpt.restore_schema = True
        options.source_driver_options = sourceGmlOpt;

        source_path = self.GetFileInBaseFolder("gml7.gml")
        destination_path = self.GetFileInOutputFolder("output_2051.gml")
        reference_path = self.GetFileInBaseFolder("output_2051.gml")

        VectorLayer.convert(source_path, Drivers.gml, destination_path, Drivers.gml, options)
        gmlOpt = GmlOptions()
        gmlOpt.restore_schema = True
        with VectorLayer.open(destination_path, Drivers.gml, gmlOpt) as layer:
            assert layer.count == 20
            assert layer.attributes.count == 2

        Comparison.compare_binary_files(destination_path, reference_path)

    # Fix TopoJSON to CSV conversion with nested properties (basic)
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-87
    # https://issue.saltov.dynabic.com/issues/GISNET-2041
    def GISNET2041_BasicTest(self):
        source_path = self.GetFileInBaseFolder("2041_input_topojson2.topojson")
        destination_path = self.GetFileInOutputFolder("output_2041_basic.csv")
        reference_path = self.GetFileInBaseFolder("output_2041_basic.csv")

        with VectorLayer.open(source_path, Drivers.topo_json) as src_layer:
            assert src_layer.count == 3
            assert any(a.name == "prop1_this" for a in src_layer.attributes)
            assert src_layer[2].get_value("prop1_this") == "that"

        VectorLayer.convert(source_path, Drivers.topo_json, destination_path, Drivers.csv)

        with VectorLayer.open(destination_path, Drivers.csv) as dst_layer:
            assert dst_layer.count == 3
            assert dst_layer.attributes.count == 4
            assert any(a.name == "prop1_this" for a in dst_layer.attributes)
            assert dst_layer[2].get_value("prop1_this") == "that"
            for i in range(3):
                assert dst_layer[i].geometry.is_empty

        Comparison.compare_binary_files(destination_path, reference_path)

    # Fix TopoJSON to CSV conversion with nested properties (with WKT column)
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-87
    # https://issue.saltov.dynabic.com/issues/GISNET-2041
    def GISNET2041_WktTest(self):
        source_path = self.GetFileInBaseFolder("2041_input_topojson2.topojson")
        destination_path = self.GetFileInOutputFolder("output_2041_wkt.csv")
        reference_path = self.GetFileInBaseFolder("output_2041_wkt.csv")

        csv_options = CsvOptions()
        csv_options.column_wkt = "GeometryWkt"

        conv_options = ConversionOptions()
        conv_options.destination_driver_options = csv_options

        VectorLayer.convert(source_path, Drivers.topo_json, destination_path, Drivers.csv, conv_options)

        with VectorLayer.open(destination_path, Drivers.csv, csv_options) as layer:
            assert layer.count == 3
            assert layer.attributes.count == 5
            assert any(a.name == "prop1_this" for a in layer.attributes)
            assert layer[2].get_value("prop1_this") == "that"

            point = layer[0].geometry
            assert abs(point.x - 102.000200020002) < 1e-12
            assert abs(point.y - 0.5000500050005) < 1e-12

            line = cast(LineString, layer[1].geometry)
            assert line.length == 4
            self._assert_coordinate(line[0], 102.000200020002, 0)
            self._assert_coordinate(line[1], 102.999799979998, 1)
            self._assert_coordinate(line[2], 103.999899989999, 0)
            self._assert_coordinate(line[3], 105, 1)

            polygon = cast(Polygon, layer[2].geometry)
            assert polygon.exterior_ring.length == 5
            self._assert_coordinate(polygon.exterior_ring[0], 100, 0)
            self._assert_coordinate(polygon.exterior_ring[1], 100, 1)
            self._assert_coordinate(polygon.exterior_ring[2], 101.000100010001, 1)
            self._assert_coordinate(polygon.exterior_ring[3], 101.000100010001, 0)
            self._assert_coordinate(polygon.exterior_ring[4], 100, 0)

        Comparison.compare_binary_files(destination_path, reference_path)

    # Helper for coordinate comparison
    def _assert_coordinate(self, point, expected_x, expected_y):
        assert abs(point.x - expected_x) < 1e-12
        assert abs(point.y - expected_y) < 1e-12

    # Add optional SRS transform error collection for invalid Shapefile conversion (no collector)
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-88
    # https://issue.saltov.dynabic.com/issues/GISNET-2042
    def GISNET2042_NoCollectorTest(self):
        source_path = self.GetFileInBaseFolder("light-traffics.shp")
        destination_path = self.GetFileInOutputFolder("output_2042_no_collector.kml")
        reference_path = self.GetFileInBaseFolder("output_2042_no_collector.kml")

        threw = False
        try:
            VectorLayer.convert(source_path, Drivers.shapefile, destination_path, Drivers.kml)
        except Exception as ex:
            if "TransformationException" in ex.args[0]:
                threw = True
            else:
                raise

        assert threw, "Expected TransformationException was not thrown"

        Comparison.compare_binary_files(destination_path, reference_path)

    # Add optional SRS transform error collection for invalid Shapefile conversion (collector)
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-88
    # https://issue.saltov.dynabic.com/issues/GISNET-2042
    def GISNET2042_WithCollectorTest(self):
        source_path = self.GetFileInBaseFolder("light-traffics.shp")
        destination_path = self.GetFileInOutputFolder("output_2042_with_collector.kml")
        reference_path = self.GetFileInBaseFolder("output_2042_with_collector.kml")

        errors = OperationErrorCollector()
        options = ConversionOptions()
        options.destination_driver_options = KmlOptions()
        options.destination_driver_options.error_collector = errors

        VectorLayer.convert(source_path, Drivers.shapefile, destination_path, Drivers.kml, options)

        assert errors.count == 1

        with VectorLayer.open(destination_path, Drivers.kml) as layer:
            assert layer.count >= 444

        Comparison.compare_binary_files(destination_path, reference_path)

    # TopoJson to Gml - QGIS does not see output
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-89
    # https://issue.saltov.dynabic.com/issues/GISNET-2047
    def GISNET2047Test(self):
        source_path = self.GetFileInBaseFolder("topojson2.json")
        destination_path = self.GetFileInOutputFolder("out.gml")
        reference_path = self.GetFileInBaseFolder("out.gml")

        VectorLayer.convert(source_path, Drivers.topo_json, destination_path, Drivers.gml)

        options = GmlOptions()
        options.restore_schema = True

        with VectorLayer.open(destination_path, Drivers.gml, options) as layer:
            print(f"Feature count: {layer.count}")
            print(f"Attribute count: {layer.attributes.count}")

            # Assertions for layer metadata
            assert layer.count == 1, f"Expected 1 feature, got {layer.count}"
            assert layer.attributes.count == 3, f"Expected 3 attributes, got {layer.attributes.count}"

            geometry = layer[0].geometry
            print(f"Geometry type: {geometry.geometry_type}")
            print(f"Geometry dimension: {geometry.dimension}")
            print(f"Geometry length: {geometry.get_length()}")

            # Assertions for geometry metadata
            assert geometry.geometry_type == 11, f"Expected geometry type 11, got {geometry.geometry_type}"
            assert geometry.dimension == 1, f"Expected dimension 1, got {geometry.dimension}"

            # Use tolerance for floating-point comparison
            expected_length = 0.3143680601002154
            actual_length = geometry.get_length()
            assert math.isclose(actual_length, expected_length, rel_tol=1e-9), \
                f"Expected length {expected_length}, got {actual_length}"

        Comparison.compare_binary_files(destination_path, reference_path)
