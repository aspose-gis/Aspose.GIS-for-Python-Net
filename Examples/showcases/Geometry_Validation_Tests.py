import os

import pytest
from aspose.gis import VectorLayer, Drivers, ConversionOptions, PointFormats, GeoConvert, GisException
from aspose.gis.formats.geojson import GeoJsonOptions
from aspose.gis.formats.topojson import TopoJsonOptions
from aspose.gis.geometries import IPoint, ILineString, Geometry, Point, LineString, GeometryCollection, CircularString, \
    CompoundCurve, ICircularString, CurvePolygon, MultiCurve, MultiLineString, MultiPoint, LinearRing, Polygon, \
    MultiPolygon, MultiSurface, GeometryType
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.FolderSettings import FolderSettings
from utils.LicenseHelper import LicenseHelper

class Geometry_Validation_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    def IsGeometryValidTest(self):
        linear_ring = LinearRing()
        linear_ring.add_point(0, 0)
        linear_ring.add_point(0, 1)
        linear_ring.add_point(1, 0)
        assert not linear_ring.is_valid

        linear_ring.add_point(0, 0)
        assert linear_ring.is_valid

    def IsGeometrySimpleTest(self):
        line_string = LineString()
        assert line_string.is_simple
        line_string.add_point(0, 0)
        line_string.add_point(1, 0)
        assert line_string.is_simple
        line_string.add_point(0.5, 0)
        assert not line_string.is_simple

    def ValidateOnWriteTest(self):
        exterior_ring = LinearRing()
        exterior_ring.add_point(0, 0)
        exterior_ring.add_point(0, 1)
        exterior_ring.add_point(1, 1)
        exterior_ring.add_point(1, 0)
        exterior_ring.add_point(0, 0)

        interior_ring = LinearRing()
        interior_ring.add_point(0.5, 0.5)
        interior_ring.add_point(1, 0.5)
        interior_ring.add_point(1, 1)
        interior_ring.add_point(0.5, 1)
        interior_ring.add_point(0.5, 0.5)

        invalid_polygon = Polygon()
        invalid_polygon.exterior_ring = exterior_ring
        invalid_polygon.add_interior_ring(interior_ring)
        # invalid_polygon.is_valid == False, since polygon rings share segments (have infinite number of intersection points)

        options = GeoJsonOptions()
        options.validate_geometries_on_write = False  # false is default
        notValidated = os.path.join(FolderSettings.BaseTestOutputFolder(), "not_validated_data_out.shp")
        #os.remove(notValidated)
        with Drivers.geo_json.create_layer(notValidated, options) as non_validating_layer:
            feature = non_validating_layer.construct_feature()
            feature.geometry = invalid_polygon
            # no exception is thrown, since validate_geometries_on_write == false, and GeoJson specification doesn't say that rings of polygon can't share segments.
            non_validating_layer.add(feature)

        options.validate_geometries_on_write = True
        validated = os.path.join(FolderSettings.BaseTestOutputFolder(), "validated_data_out.shp")
        #os.remove(validated)
        with Drivers.geo_json.create_layer(validated, options) as validating_layer:
            feature = validating_layer.construct_feature()
            feature.geometry = invalid_polygon
            wasException = False
            try:
                validating_layer.add(feature)  # GisException is thrown, since polygon is not valid
            except Exception as e:
                wasException = True
            if not wasException:
                raise

    def ValidateOnWriteObeyingSpecificationsTest(self):
        line_string_with_one_point = LineString()
        line_string_with_one_point.add_point(0, 0)

        options = GeoJsonOptions()
        options.validate_geometries_on_write = False
        file = os.path.join(FolderSettings.BaseTestOutputFolder(), "ValidateOnWriteObeyingSpecifications_out.json")
        with Drivers.geo_json.create_layer(file, options) as layer:
            feature = layer.construct_feature()
            # GeoJSON specification says that line string must have at least two coordinates.
            feature.geometry = line_string_with_one_point
            wasException = False
            try:
                # Geometry of feature doesn't match data format specification, so exception is thrown
                # regardless of what validate_geometries_on_write option is.
                layer.add(feature)
            except Exception as e:
                wasException = True
            if not wasException:
                raise
