import os
from decimal import Decimal

import pytest
from aspose.gis import VectorLayer, Drivers, ConversionOptions, PointFormats, GeoConvert, GisException, PrecisionModel, \
    NumericFormat
from aspose.gis.formats.geojson import GeoJsonOptions
from aspose.gis.formats.shapefile import ShapefileOptions
from aspose.gis.formats.topojson import TopoJsonOptions
from aspose.gis.geometries import IPoint, ILineString, Geometry, Point, LineString, GeometryCollection, CircularString, \
    CompoundCurve, ICircularString, CurvePolygon, MultiCurve, MultiLineString, MultiPoint, LinearRing, Polygon, \
    MultiPolygon, MultiSurface, GeometryType, WkbVariant, WktVariant
from aspose.gis.spatialreferencing import SpatialReferenceSystem
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.FolderSettings import FolderSettings
from utils.LicenseHelper import LicenseHelper
class Geometry_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Convert GeoJson To TopoJson
    def ConvertCoordinatesTest(self):
        decimal_degrees = GeoConvert.as_point_text(25.5, 45.5, PointFormats.DECIMAL_DEGREES)
        print(decimal_degrees)
        assert decimal_degrees == '25.5°, 045.5°'

        degree_decimal_minutes = GeoConvert.as_point_text(25.5, 45.5, PointFormats.DEGREE_DECIMAL_MINUTES)
        print(degree_decimal_minutes)
        assert degree_decimal_minutes == "25°30', 045°30'"

        degree_minutes_seconds = GeoConvert.as_point_text(25.5, 45.5, PointFormats.DEGREE_MINUTES_SECONDS)
        print(degree_minutes_seconds)
        assert degree_minutes_seconds == "25°30'00\", 045°30'00\""

        geo_ref = GeoConvert.as_point_text(25.5, 45.5, PointFormats.GEO_REF)
        print(degree_minutes_seconds)
        assert geo_ref == 'RHAL30003000'

        mgrs = GeoConvert.as_point_text(25.5, 45.5, PointFormats.MGRS)
        print(mgrs)
        assert mgrs == '38RNP5024920408'

        usng = GeoConvert.as_point_text(25.5, 45.5, PointFormats.USNG)
        print(usng)
        assert usng == '38RNP5024920408'

    def ParseCoordinateTest(self):
        outPoint = []
        GeoConvert.try_parse_point_text("25.5°, 45.5°", outPoint)
        point = cast(IPoint, outPoint[0])
        assert point.x == 45.5, point.y == 25.5

        GeoConvert.try_parse_point_text("25°30.00000', 045°30.00000'", outPoint)
        point = cast(IPoint, outPoint[0])
        assert point.x == 45.5, point.y == 25.5

        GeoConvert.try_parse_point_text("25°30'00.3000\", 045°30'00.3000\"", outPoint)
        point = cast(IPoint, outPoint[0])
        assert abs(point.x - 45.5) < 0.001, abs(point.y - 25.5) < 0.001

        GeoConvert.try_parse_point_text("RHAL30003000", outPoint)
        point = cast(IPoint, outPoint[0])
        assert point.x == 45.5, point.y == 25.5

        print(point)

    def ConvertGeometryToEditableTest(self):
        # Create a read-only LineString
        read_only_line = cast(ILineString, Geometry.from_text("LINESTRING (1 1, 2 2)"))

        # LineString in Shapely is already editable, so we can directly work with it
        editable_line = read_only_line.to_editable()

        # Adding a new point to the LineString
        editable_line.add_point(3, 3)

        # Print the modified LineString
        print(editable_line.as_text())  # LINESTRING (1 1, 2 2, 3 3)
        assert editable_line.as_text() == "LINESTRING (1 1, 2 2, 3 3)"

        # The initial geometry remains unchanged
        print(read_only_line.as_text())  # LINESTRING (1 1, 2 2)
        assert read_only_line.as_text() == "LINESTRING (1 1, 2 2)"

    def CountGeometriesInGeometryTest(self):
        # Create a Point
        point = Point(40.7128, -74.006)

        # Create a LineString and add points to it
        line = LineString()
        line.add_point(78.65, -32.65)
        line.add_point(-98.65, 12.65)

        # Create a GeometryCollection and add geometries to it
        geometry_collection = GeometryCollection()
        geometry_collection.add(point)
        geometry_collection.add(line)

        # Count the geometries in the collection
        geometries_count = geometry_collection.count
        print(geometries_count)  # Output: 2
        assert geometries_count == 2
        assert str(geometry_collection) == "GEOMETRYCOLLECTION (POINT (40.7128 -74.006), LINESTRING (78.65 -32.65, -98.65 12.65))"

    def CountPointsInGeometryTest(self):
        line = LineString()
        line.add_point(78.65, -32.65)
        line.add_point(-98.65, 12.65)
        pointsCount = len(line)

        assert pointsCount == 2

    def CreateCircularStringTest(self):
        outputPath = os.path.join(FolderSettings.BaseTestOutputFolder(), "CreateCircularString_out.shp")
        referencePath = os.path.join(FolderSettings.CommonReferenceTestFolder(), "CreateCircularString_out.shp")
        with VectorLayer.create(outputPath, Drivers.shapefile) as layer:
            feature = layer.construct_feature()
            circularString = CircularString()
            circularString.add_point(0, 0)
            circularString.add_point(1, 1)
            circularString.add_point(2, 0)
            circularString.add_point(1, -1)
            circularString.add_point(0, 0)
            feature.geometry = circularString

            layer.add(feature)

        Comparison.compare_binary_files(referencePath, outputPath)

    def CreateCompountCurveTest(self):
        outputPath = os.path.join(FolderSettings.BaseTestOutputFolder(), "CreateCompoundCurve_out.shp")
        referencePath = os.path.join(FolderSettings.CommonReferenceTestFolder(), "CreateCompoundCurve_out.shp")
        with VectorLayer.create(outputPath, Drivers.shapefile) as layer:
            feature = layer.construct_feature()

            # create an 'S' letter (starts at bottom left end)
            compoundCurve = CompoundCurve()

            bottom = cast(ILineString, Geometry.from_text("LineString (0 0, 3 0)"))
            firstArc =  cast(ICircularString, Geometry.from_text("CircularString (3 0, 4 1, 3 2)"))
            middle =  cast(ILineString, Geometry.from_text("LineString (3 2, 1 2)"))
            secondArc =  cast(ICircularString, Geometry.from_text("CircularString (1 2, 0 3, 1 4)"))
            top =  cast(ILineString, Geometry.from_text("LineString (1 4, 4 4)"))

            compoundCurve.add_curve(bottom)
            compoundCurve.add_curve(firstArc)
            compoundCurve.add_curve(middle)
            compoundCurve.add_curve(secondArc)
            compoundCurve.add_curve(top)

            feature.geometry = compoundCurve
            layer.add(feature)

        Comparison.compare_binary_files(referencePath, outputPath)

    def CreateCurvePolygonTest(self):
        outputPath = os.path.join(FolderSettings.BaseTestOutputFolder(), "CreateCurvePolygon_out.shp")
        referencePath = os.path.join(FolderSettings.CommonReferenceTestFolder(), "CreateCurvePolygon_out.shp")
        with VectorLayer.create(outputPath, Drivers.shapefile) as layer:
            feature = layer.construct_feature()

            # create a torus with center at (0,0), radius equal to 2 and hole radius equal to 1
            curvePolygon = CurvePolygon()

            exterior = CircularString()
            exterior.add_point(-2, 0)
            exterior.add_point(0, 2)
            exterior.add_point(2, 0)
            exterior.add_point(0, -2)
            exterior.add_point(-2, 0)

            curvePolygon.exterior_ring = exterior

            interior = CircularString()
            interior.add_point(-1, 0)
            interior.add_point(0, 1)
            interior.add_point(1, 0)
            interior.add_point(0, -1)
            interior.add_point(-1, 0)

            curvePolygon.add_interior_ring(interior)
            feature.geometry = curvePolygon

            layer.add(feature)

        Comparison.compare_binary_files(referencePath, outputPath)

    def CreateGeometryCollectionTest(self):
        point = Point(40.7128, -74.006)

        line = LineString()
        line.add_point(78.65, -32.65)
        line.add_point(-98.65, 12.65)

        geometryCollection = GeometryCollection()
        geometryCollection.add(point)
        geometryCollection.add(line)

        print(geometryCollection)
        assert str(geometryCollection) == "GEOMETRYCOLLECTION (POINT (40.7128 -74.006), LINESTRING (78.65 -32.65, -98.65 12.65))"

    def CreateLineStringTest(self):
        line = LineString()
        line.add_point(78.65, -32.65)
        line.add_point(-98.65, 12.65)

        print(line)
        assert str(line) == "LINESTRING (78.65 -32.65, -98.65 12.65)"

    def CreateMultiCurveTest(self):
        outputPath = os.path.join(FolderSettings.BaseTestOutputFolder(), "CreateMultiCurve_out.shp")
        referencePath = os.path.join(FolderSettings.CommonReferenceTestFolder(), "CreateMultiCurve_out.shp")
        with VectorLayer.create(outputPath, Drivers.shapefile) as layer:
            feature = layer.construct_feature()
            multiCurve = MultiCurve()
            multiCurve.add(Geometry.from_text("LineString (0 0, 1 0)"))
            multiCurve.add(Geometry.from_text("CircularString (2 2, 3 3, 4 2)"))
            multiCurve.add(Geometry.from_text("CompoundCurve ((0 1, 0 0), CircularString (0 0, 3 3, 6 0))"))
            feature.geometry = multiCurve

            layer.add(feature)

        Comparison.compare_binary_files(referencePath, outputPath)

    def CreateMultiLineStringTest(self):
        firstLine = LineString()
        firstLine.add_point(7.5, -3.5)
        firstLine.add_point(-9.6, 12.6)

        secondLine = LineString()
        secondLine.add_point(8.5, -2.6)
        secondLine.add_point(-8.6, 1.5)

        multiLineString = MultiLineString()
        multiLineString.add(firstLine)
        multiLineString.add(secondLine)

        print(multiLineString)
        assert str(multiLineString) == "MULTILINESTRING ((7.5 -3.5, -9.6 12.6), (8.5 -2.6, -8.6 1.5))"

    def CreateMultiPointTest(self):
        multipoint = MultiPoint()
        multipoint.add(Point(1, 2))
        multipoint.add(Point(3, 4))

        print(multipoint)
        assert str(multipoint) == "MULTIPOINT ((1 2), (3 4))"

    def CreateMultiPolygonTest(self):
        firstRing = LinearRing()
        firstRing.add_point(8.5, -2.5)
        firstRing.add_point(-8.5, 2.5)
        firstRing.add_point(8.5, -2.5)
        firstPolygon = Polygon(firstRing)

        secondRing = LinearRing()
        secondRing.add_point(7.6, -3.6)
        secondRing.add_point(-9.6, 1.5)
        secondRing.add_point(7.6, -3.6)
        secondPolygon = Polygon(secondRing)

        multiPolygon = MultiPolygon()
        multiPolygon.add(firstPolygon)
        multiPolygon.add(secondPolygon)

        print(multiPolygon)
        assert str(multiPolygon) == "MULTIPOLYGON (((8.5 -2.5, -8.5 2.5, 8.5 -2.5)), ((7.6 -3.6, -9.6 1.5, 7.6 -3.6)))"

    def CreateMultiSurfaceTest(self):
        outputPath = os.path.join(FolderSettings.BaseTestOutputFolder(), "CreateMultiSurface_out.json")
        referencePath = os.path.join(FolderSettings.CommonReferenceTestFolder(), "CreateMultiSurface_out.json")
        with VectorLayer.create(outputPath, Drivers.geo_json) as layer:
            feature = layer.construct_feature()
            multiSurface = MultiSurface()

            polygon = Geometry.from_text("Polygon ((0 0, 0 1, 1 1, 1 0, 0 0))")
            multiSurface.add(polygon)

            curvePolygon = Geometry.from_text("CurvePolygon (CircularString (-2 0, 0 2, 2 0, 0 -2, -2 0))")
            multiSurface.add(curvePolygon)

            feature.geometry = multiSurface
            layer.add(feature)
            print(str(feature.geometry))
            assert str(feature.geometry) == "MULTISURFACE (((0 0, 0 1, 1 1, 1 0, 0 0)), CURVEPOLYGON (CIRCULARSTRING (-2 0, 0 2, 2 0, 0 -2, -2 0)))"

        Comparison.compare_binary_files(referencePath, outputPath)

    def CreatePointTest(self):
        point = Point(40.7128, -74.006)
        print(point)
        assert str(point) == "POINT (40.7128 -74.006)"

    def CreatePolygonTest(self):
        polygon = Polygon()

        ring = LinearRing()
        ring.add_point(50.02, 36.22)
        ring.add_point(49.99, 36.26)
        ring.add_point(49.97, 36.23)
        ring.add_point(49.98, 36.17)
        ring.add_point(50.02, 36.22)

        polygon.exterior_ring = ring

        print(polygon)
        assert str(polygon) == "POLYGON ((50.02 36.22, 49.99 36.26, 49.97 36.23, 49.98 36.17, 50.02 36.22))"

    def CreatePolygonWithHoleTest(self):
        polygon = Polygon()

        ring = LinearRing()
        ring.add_point(50.02, 36.22)
        ring.add_point(49.99, 36.26)
        ring.add_point(49.97, 36.23)
        ring.add_point(49.98, 36.17)
        ring.add_point(50.02, 36.22)

        hole = LinearRing()
        hole.add_point(50.00, 36.22)
        hole.add_point(49.99, 36.20)
        hole.add_point(49.98, 36.23)
        hole.add_point(50.00, 36.24)
        hole.add_point(50.00, 36.22)

        polygon.exterior_ring = ring
        polygon.add_interior_ring(hole)

        print(polygon)
        assert str(polygon) == "POLYGON ((50.02 36.22, 49.99 36.26, 49.97 36.23, 49.98 36.17, 50.02 36.22), (50 36.22, 49.99 36.2, 49.98 36.23, 50 36.24, 50 36.22))"

    def DetermineIfGeometriesAreSpatiallyEqualTest(self):
        geometry1 = MultiLineString()
        lineStr1 = LineString()
        lineStr1.add_point(Point(0, 0))
        lineStr1.add_point(Point(1, 1))

        lineStr2 = LineString()
        lineStr2.add_point(Point(1, 1))
        lineStr2.add_point(Point(2, 2))


        geometry1.add(lineStr1)
        geometry1.add(lineStr2)

        lineStr3 = LineString()
        lineStr3.add_point(Point(0, 0))
        lineStr3.add_point(Point(2, 2))
        geometry2 = lineStr3

        print(geometry1.spatially_equals(geometry2))  # True
        assert geometry1.spatially_equals(geometry2)

        geometry2.add_point(3, 3)
        print(geometry1.spatially_equals(geometry2))  # False
        assert not geometry1.spatially_equals(geometry2)

    def DetermineIfGeometriesCrossEachOtherTest(self):
        geometry1 = LineString()
        geometry1.add_point(0, 0)
        geometry1.add_point(2, 2)

        geometry2 = LineString()
        geometry2.add_point(1, 1)
        geometry2.add_point(3, 3)

        print(geometry1.crosses(geometry2))  # False
        assert not geometry1.crosses(geometry2)

        geometry3 = LineString()
        geometry3.add_point(0, 2)
        geometry3.add_point(2, 0)

        print(geometry1.crosses(geometry3))  # True
        assert geometry1.crosses(geometry3)

    def DetermineIfGeometriesIntersectTest(self):
        ring1 = LinearRing()
        ring1.add_point(Point(0, 0))
        ring1.add_point(Point(0, 3))
        ring1.add_point(Point(3, 3))
        ring1.add_point(Point(3, 0))
        ring1.add_point(Point(0, 0))

        geometry1 = Polygon(ring1)


        ring2 = LinearRing()
        ring2.add_point(Point(1, 1))
        ring2.add_point(Point(1, 4))
        ring2.add_point(Point(4, 4))
        ring2.add_point(Point(4, 1))
        ring2.add_point(Point(1, 1))

        geometry2 = Polygon(ring2)


        print(geometry1.intersects(geometry2))  # True
        assert geometry1.intersects(geometry2)
        print(geometry2.intersects(geometry1))  # True
        assert geometry2.intersects(geometry1)

        # 'Disjoint' is opposite to 'Intersects'
        print(geometry1.disjoint(geometry2))  # False
        assert not geometry1.disjoint(geometry2)

    def DetermineIfGeometriesOverlapTest(self):
        geometry1 = LineString()
        geometry1.add_point(0, 0)
        geometry1.add_point(0, 2)

        geometry2 = LineString()
        geometry2.add_point(0, 2)
        geometry2.add_point(0, 3)

        print(geometry1.overlaps(geometry2))  # False
        assert not geometry1.overlaps(geometry2)

        geometry3 = LineString()
        geometry3.add_point(0, 1)
        geometry3.add_point(0, 3)

        print(geometry1.overlaps(geometry3))  # True
        assert geometry1.overlaps(geometry3)

    def DetermineIfGeometriesTouchEachOtherTest(self):
        geometry1 = LineString()
        geometry1.add_point(0, 0)
        geometry1.add_point(2, 2)

        geometry2 = LineString()
        geometry2.add_point(2, 2)
        geometry2.add_point(3, 3)

        print(geometry1.touches(geometry2))  # True
        assert geometry1.touches(geometry2)
        print(geometry2.touches(geometry1))  # True
        assert geometry2.touches(geometry1)

        geometry3 = Point(2, 2)
        print(geometry1.touches(geometry3))  # True
        assert geometry1.touches(geometry3)


        geometry4 = LineString()
        geometry4.add_point(1, 1)
        geometry4.add_point(4, 4)

        print(geometry1.touches(geometry4))  # False
        assert not geometry1.touches(geometry4)

    def DetermineIfGeometryHasCurvesTest(self):
        geometry_without_curves = Geometry.from_text(
            "GeometryCollection (LineString (0 0, 1 1, 2 0), CompoundCurve ((4 0, 5 1), (5 1, 6 2, 7 1)))")
        # geometry does not contain circular string, so has_curve_geometry returns false.
        print(geometry_without_curves.has_curve_geometry)  # False
        assert not geometry_without_curves.has_curve_geometry

        geometry = Geometry.from_text(
            "GeometryCollection (LineString (0 0, 1 1, 2 0), CompoundCurve ((4 0, 5 1), CircularString (5 1, 6 2, 7 1)))")
        # geometry contains circular string, so has_curve_geometry returns true.
        print(geometry.has_curve_geometry)  # True
        assert geometry.has_curve_geometry

    def DetermineIfOneGeometryCoversAnotherTest(self):
        line = LineString()
        line.add_point(0, 0)
        line.add_point(1, 1)

        point = Point(0, 0)
        print(line.covers(point))  # True
        print(point.covered_by(line))  # True

        assert line.covers(point)
        assert point.covered_by(line)

    def DetermineSpatialRelationViaRelateMethodTest(self):
        geometry1 = LineString()
        geometry1.add_point(0, 0)
        geometry1.add_point(0, 2)

        geometry2 = LineString()
        geometry2.add_point(0, 1)
        geometry2.add_point(0, 3)

        # Relate method takes a string representation of DE-9IM matrix
        # (Dimensionally Extended Nine-Intersection Model matrix).
        # see Simple Feature Access specification for more details on DE-9IM.

        # this is the equivalent of 'geometry1.spatially_equals(geometry2)'
        print(geometry1.relate(geometry2, "T*F**FFF*"))  # False
        assert not geometry1.relate(geometry2, "T*F**FFF*")

        # this is the equivalent of 'geometry1.disjoint(geometry2)'
        print(geometry1.relate(geometry2, "FF*FF****"))  # False
        assert not geometry1.relate(geometry2, "FF*FF****")

        # this is the equivalent of 'geometry1.overlaps(geometry2)'
        print(geometry1.relate(geometry2, "1*T***T**"))  # True
        assert geometry1.relate(geometry2, "1*T***T**")

    def FindOverlaysOfGeometriesTest(self):
        # find intersection, union, difference and symmetric difference of two geometries.
        polygon1 = Polygon()

        ring1 = LinearRing()
        ring1.add_point(Point(0, 0))
        ring1.add_point(Point(0, 2))
        ring1.add_point(Point(2, 2))
        ring1.add_point(Point(2, 0))
        ring1.add_point(Point(0, 0))
        polygon1.exterior_ring = ring1

        polygon2 = Polygon()
        ring2 = LinearRing()
        ring2.add_point(Point(1, 1))
        ring2.add_point(Point(1, 3))
        ring2.add_point(Point(3, 3))
        ring2.add_point(Point(3, 1))
        ring2.add_point(Point(1, 1))
        polygon2.exterior_ring = ring2

        intersection = polygon1.intersection(polygon2)
        print("Intersection type is {0}".format(intersection.geometry_type))  # Polygon
        assert intersection.geometry_type == GeometryType.POLYGON
        assert str(intersection.exterior_ring) == "LINESTRING (1 2, 2 2, 2 1, 1 1, 1 2)"

        union = polygon1.union(polygon2)
        print("Union type is {0}".format(union.geometry_type))  # Polygon
        assert union.geometry_type == GeometryType.POLYGON
        assert str(union.exterior_ring) == "LINESTRING (0 0, 0 2, 1 2, 1 3, 3 3, 3 1, 2 1, 2 0, 0 0)"

        difference = polygon1.difference(polygon2)
        print("Difference type is {0}".format(difference.geometry_type))  # Polygon
        assert difference.geometry_type == GeometryType.POLYGON
        assert str(difference.exterior_ring) == "LINESTRING (0 0, 0 2, 1 2, 1 1, 2 1, 2 0, 0 0)"


        sym_difference = polygon1.sym_difference(polygon2)
        print("Symmetric Difference type is {0}".format(sym_difference.geometry_type))  # MultiPolygon
        assert sym_difference.geometry_type == GeometryType.MULTI_POLYGON
        multi_polygon = cast(MultiPolygon, sym_difference)  # Assuming sym_difference is already a MultiPolygon
        print("Polygons count is {0}".format(multi_polygon.count))  # 2
        assert multi_polygon.count == 2
        assert str(multi_polygon[0].exterior_ring) == "LINESTRING (0 0, 0 2, 1 2, 1 1, 2 1, 2 0, 0 0)"
        assert str(multi_polygon[1].exterior_ring) == "LINESTRING (2 1, 2 2, 1 2, 1 3, 3 3, 3 1, 2 1)"

    def GeometryValidationTest(self):
        line_str_with_one_point = LineString()
        line_str_with_one_point.add_point(0, 0)

        options = GeoJsonOptions()
        options.validate_geometries_on_write = False

        output_path = os.path.join(FolderSettings.BaseTestOutputFolder(),
                                   "ValidateOnWriteObeyingSpecifications_out.json")

        # Creating the layer with the output path inside the with statement
        with Drivers.geo_json.create_layer(output_path, options) as layer:
            feature = layer.construct_feature()
            # GeoJSON specification says that line string must have at least two coordinates.
            feature.geometry = line_str_with_one_point

            wasException = False
            try:
                # Geometry of feature doesn't match data format specification, so exception is thrown
                # regardless of what validate_geometries_on_write option is.
                layer.add(feature)
            except Exception as e:
                wasException = True
                print(e)
            if not wasException:
                raise "There was not be exception but it should be"

    def GetAreaOfGeometryTest(self):
        # Create the triangle ring
        triangle_ring = LinearRing()
        triangle_ring.add_point(4, 6)
        triangle_ring.add_point(1, 3)
        triangle_ring.add_point(8, 7)
        triangle_ring.add_point(4, 6)
        triangle = Polygon(triangle_ring)

        # Create the square ring
        square_ring = LinearRing()
        square_ring.add_point(0, 9)
        square_ring.add_point(0, 7)
        square_ring.add_point(2, 7)
        square_ring.add_point(2, 9)
        square_ring.add_point(0, 9)
        square = Polygon(square_ring)

        # Create the multi-polygon
        multi_polygon = MultiPolygon()
        multi_polygon.add(triangle)
        multi_polygon.add(square)

        # Print areas formatted to two decimal places
        print(f"{triangle.get_area():.2f}")  # 4.50
        assert f"{triangle.get_area():.2f}" == "4.50"

        print(f"{square.get_area():.2f}")  # 4.00
        assert f"{square.get_area():.2f}" == "4.00"

        print(f"{multi_polygon.get_area():.2f}")  # 8.50
        assert f"{multi_polygon.get_area():.2f}" == "8.50"

    def GetCentroidTest(self):
        # Create the polygon
        polygon = Polygon()
        ring = LinearRing()
        ring.add_point(1, 0)
        ring.add_point(2, 2)
        ring.add_point(0, 4)
        ring.add_point(5, 5)
        ring.add_point(6, 1)
        ring.add_point(1, 0)

        polygon.exterior_ring = ring

        # Get the centroid of the polygon
        centroid = polygon.get_centroid()

        # Print centroid coordinates formatted to two decimal places
        print(f"{centroid.x:.2f} {centroid.y:.2f}")  # 3.33 2.58
        assert f"{centroid.x:.2f} {centroid.y:.2f}" == "3.33 2.58"

    def GetConvexHullOfGometryTest(self):
        # Assuming appropriate imports for MultiPoint, Point, and ILinearRing are done

        # Create the geometry
        geometry = MultiPoint()
        geometry.add(Point(3, 2))
        geometry.add(Point(0, 0))
        geometry.add(Point(6, 5))
        geometry.add(Point(5, 10))
        geometry.add(Point(10, 0))
        geometry.add(Point(8, 2))
        geometry.add(Point(4, 3))

        # Get the convex hull
        convex_hull = geometry.get_convex_hull()

        # Assuming convex_hull can be cast or is directly usable as ILinearRing
        ring = convex_hull  # Adjust this if necessary based on your library
        assert str(ring) == "LINESTRING (0 0, 5 10, 10 0, 0 0)"

    def GetDistanceBetweenGeometriesTest(self):
        # Create the polygon
        polygon = Polygon()

        ring = LinearRing()
        ring.add_point(0, 0)
        ring.add_point(0, 1)
        ring.add_point(1, 1)
        ring.add_point(1, 0)
        ring.add_point(0, 0)

        polygon.exterior_ring = ring

        # Create the line string
        line = LineString()
        line.add_point(2, 0)
        line.add_point(1, 3)

        # Calculate the distance from the polygon to the line
        distance = polygon.get_distance_to(line)

        # Print the distance formatted to two decimal places
        print(f"{distance:.2f}")  # 0.63
        assert f"{distance:.2f}" == "0.63"

    def GetGeometryBufferTest(self):
        # Assuming appropriate imports for LineString, Polygon, LinearRing, Point, and IPolygon are done

        # Create the line string
        line = LineString()
        line.add_point(0, 0)
        line.add_point(3, 3)

        # Buffer with positive distance contains all points whose distance to input geometry is less or equal to 'distance' argument
        line_buffer = line.get_buffer(1, 30)

        print(line_buffer.spatially_contains(Point(1, 2)))  # True
        assert line_buffer.spatially_contains(Point(1, 2))
        print(line_buffer.spatially_contains(Point(3.1, 3.1)))  # True
        assert line_buffer.spatially_contains(Point(3.1, 3.1))

        # Create the polygon
        polygon = Polygon()
        ring = LinearRing()
        ring.add_point(0, 0)
        ring.add_point(0, 3)
        ring.add_point(3, 3)
        ring.add_point(3, 0)
        ring.add_point(0, 0)

        polygon.exterior_ring = ring

        # Buffer with negative distance 'shrinks' geometry
        polygon_buffer = polygon.get_buffer(-1, 30)

        # Assuming polygon_buffer has an attribute or method for accessing the exterior ring
        assert str(polygon_buffer) == "POLYGON ((1 1, 1 2, 2 2, 2 1, 1 1))"

    def GetGeometryTypeTest(self):
        point = Point(40.7128, -74.006)
        geometry_type = point.geometry_type

        print(geometry_type)  # Point
        assert str(point) == "POINT (40.7128 -74.006)"
        assert geometry_type == GeometryType.POINT

    def GetLengthOfGeometryTest(self):
        line = LineString()
        line.add_point(0, 0)
        line.add_point(2, 2)
        line.add_point(2, 0)

        print("{:.2f}".format(line.get_length()))  # 4.83
        assert "{:.2f}".format(line.get_length()) == "4.83"
        rectangle = Polygon()
        ring = LinearRing()
        ring.add_point(0, 0)
        ring.add_point(0, 1)
        ring.add_point(1, 1)
        ring.add_point(1, 0)
        ring.add_point(0, 0)
        rectangle.add_interior_ring(ring)

        # GetLength() returns perimeter for polygons
        print("{:.2f}".format(rectangle.get_length()))  # 4.00
        assert "{:.2f}".format(rectangle.get_length()) == "4.00"

    def GetPointOnSurfaceTest(self):
        polygon = Polygon()
        ring = LinearRing()
        ring.add_point(0, 0)
        ring.add_point(0, 1)
        ring.add_point(1, 1)
        ring.add_point(0, 0)

        polygon.exterior_ring = ring

        point_on_surface = polygon.get_point_on_surface()

        # point on surface is guaranteed to be inside a polygon.
        print(polygon.spatially_contains(point_on_surface))  # True
        assert polygon.spatially_contains(point_on_surface)

    def IterateOverGeometriesInGeometryTest(self):
        point_geometry = Point(40.7128, -74.006)
        line_geometry = LineString()
        line_geometry.add_point(78.65, -32.65)
        line_geometry.add_point(-98.65, 12.65)
        geometry_collection = GeometryCollection()
        geometry_collection.add(point_geometry)
        geometry_collection.add(line_geometry)

        for geometry in geometry_collection:
            if geometry.geometry_type == GeometryType.POINT:
                point = geometry
                assert str(point) == "POINT (40.7128 -74.006)"
            elif geometry.geometry_type == GeometryType.LINE_STRING:
                line = geometry
                assert str(line) == "LINESTRING (78.65 -32.65, -98.65 12.65)"
    def IterateOverPointsInGeometryTest(self):
        line = LineString()
        line.add_point(78.65, -32.65)
        line.add_point(-98.65, 12.65)

        for point in line:
            print(f"{point.x},{point.y}")

        assert str(line) == "LINESTRING (78.65 -32.65, -98.65 12.65)"

    def LimitPrecisionWhenReadingGeometriesTest(self):
        path = os.path.join(FolderSettings.BaseTestOutputFolder(), "LimitPrecisionWhenReadingGeometries_out.shp")
        with VectorLayer.create(path, Drivers.shapefile) as layer:
            feature = layer.construct_feature()
            feature.geometry = Point(1.10234, 2.09743)
            layer.add(feature)

        options = ShapefileOptions()
        # read data as-is.
        options.xy_precision_model = PrecisionModel.exact

        with VectorLayer.open(path, Drivers.shapefile, options) as layer:
            point = layer[0].geometry
            # 1.10234, 2.09743
            print(f"{point.x}, {point.y}")
            assert f"{point.x}, {point.y}" == "1.10234, 2.09743"

        # truncate all X and Y, so only two fractional digits are left.
        options.xy_precision_model = PrecisionModel.rounding(2)

        with VectorLayer.open(path, Drivers.shapefile, options) as layer:
            point = layer[0].geometry
            # 1.1, 2.1
            print(f"{point.x}, {point.y}")
            assert f"{point.x}, {point.y}" == "1.1, 2.1"

    def LimitPrecisionWhenWritingGeometriesTest(self):
        options = GeoJsonOptions()
        options.xy_precision_model = PrecisionModel.rounding(3)
        options.z_precision_model = PrecisionModel.exact

        path = os.path.join(FolderSettings.BaseTestOutputFolder(), "LimitPrecisionWhenWritingGeometries_out.json")
        with VectorLayer.create(path, Drivers.geo_json, options) as layer:
            point = Point()
            point.x = 1.8888888
            point.y = 1.00123
            point.z = 1.123456789

            feature = layer.construct_feature()
            feature.geometry = point
            layer.add(feature)

        with VectorLayer.open(path, Drivers.geo_json) as layer:
            point = layer[0].geometry

            # 1.889, 1.001, 1.123456789
            print(f"{point.x}, {point.y}, {point.z}")
            assert f"{point.x}, {point.y}, {point.z}" == "1.889, 1.001, 1.123456789"

    def LinearizeGeometryTest(self):
        path = os.path.join(FolderSettings.BaseTestOutputFolder(), "LinearizeGeometry_out.kml")
        referencePath = os.path.join(FolderSettings.CommonTestFolder(), "LinearizeGeometry_out.kml")
        with Drivers.kml.create_layer(path) as layer:
            feature = layer.construct_feature()
            geometry = Geometry.from_text("GeometryCollection (LineString (0 0, 1 1, 2 0),CompoundCurve ((4 0, 5 1), CircularString (5 1, 6 2, 7 1)))")
            # creates linear geometry that approximates input geometry
            linear = geometry.to_linear_geometry()
            feature.geometry = linear

            layer.add(feature)
        Comparison.compare_binary_files(referencePath, path)

    def ReducePrecisionOfAGeometryTest(self):
        point = Point(1.344, 2.345, 3.345, 4.545)
        point.round_xy(digits=2)

        # 1.34, 2.35, 3.345, 4.545
        print(f"{point.x}, {point.y}, {point.z}, {point.m}")
        assert f"{point.x}, {point.y}, {point.z}, {point.m}" == "1.34, 2.35, 3.345, 4.545"

        point.round_z(digits=1)

        # 1.34, 2.35, 3.3, 4.345
        print(f"{point.x}, {point.y}, {point.z}, {point.m}")
        assert f"{point.x}, {point.y}, {point.z}, {point.m}" == "1.34, 2.35, 3.3, 4.545"

        line = LineString()
        line.add_point(1.2, 2.3)
        line.add_point(2.4, 3.5)
        line.round_xy(digits=0)

        # 1, 2
        print(f"{Decimal(line[0].x).normalize()}, {Decimal(line[0].y).normalize()}")
        assert f"{Decimal(line[0].x).normalize()}, {Decimal(line[0].y).normalize()}" == "1, 2"
        # 2, 3
        print(f"{Decimal(line[1].x).normalize()}, {Decimal(line[1].y).normalize()}")
        assert f"{Decimal(line[1].x).normalize()}, {Decimal(line[1].y).normalize()}" == "2, 4"

    def ReplacePolygonsByLinesTest(self):
        src_geometry = Geometry.from_text("GeometryCollection (POLYGON((1 2, 1 4, 3 4, 3 2)), Point (5 1))")
        dst_geometry = src_geometry.replace_polygons_by_lines()
        print(f"source: {src_geometry.as_text()}")
        assert src_geometry.as_text() == "GEOMETRYCOLLECTION (POLYGON ((1 2, 1 4, 3 4, 3 2)), POINT (5 1))"
        print(f"result: {dst_geometry.as_text()}")
        assert dst_geometry.as_text() == "GEOMETRYCOLLECTION (LINESTRING (1 2, 1 4, 3 4, 3 2, 1 2), POINT (5 1))"

    def SpecifyLinearizationToleranceTest(self):
        # If file format does not support curve geometries, we linearize them on write.
        # This example shows how to specify tolerance of the linearization.

        options = GeoJsonOptions()
        options.linearization_tolerance = 1e-4

        path = os.path.join(FolderSettings.BaseTestOutputFolder(), "SpecifyLinearizationTolerance_out.json")
        referencePath = os.path.join(FolderSettings.CommonTestFolder(), "SpecifyLinearizationTolerance_out.json")
        with VectorLayer.create(path, Drivers.geo_json, options) as layer:
            curve_geometry = Geometry.from_text("CircularString (0 0, 1 1, 2 0)")
            feature = layer.construct_feature()
            feature.geometry = curve_geometry
            # geometry is linearized with tolerance 1e-4
            layer.add(feature)

        Comparison.compare_binary_files(referencePath, path)

    def SpecifyWkbVariantOnTranslationTest(self):
        path = os.path.join(FolderSettings.BaseTestOutputFolder(), "EWkbFile.ewkb")
        referencePath = os.path.join(FolderSettings.CommonTestFolder(), "EWkbFileRef.ewkb")
        geometry = Geometry.from_text("LINESTRING (1.2 3.4, 5.6 7.8)")
        wkb = geometry.as_binary(WkbVariant.EXTENDED_POST_GIS)
        with open(path, "wb") as f:
            f.write(wkb)

        Comparison.compare_binary_files(referencePath, path)

    def SpecifyWktVariantOnTranslationTest(self):
        point = Point(23.5732, 25.3421)
        point.m = 40.3
        point.spatial_reference_system = SpatialReferenceSystem.wgs84

        print(point.as_text(WktVariant.ISO))  # POINT M (23.5732, 25.3421, 40.3)
        assert point.as_text(WktVariant.ISO) == "POINT M (23.5732 25.3421 40.3)"
        print(point.as_text(WktVariant.SIMPLE_FEATURE_ACCESS_OUTDATED))  # POINT (23.5732, 25.3421)
        assert point.as_text(WktVariant.SIMPLE_FEATURE_ACCESS_OUTDATED) == "POINT (23.5732 25.3421)"
        print(point.as_text(WktVariant.EXTENDED_POST_GIS))  # SRID=4326;POINTM (23.5732, 25.3421, 40.3)
        assert point.as_text(WktVariant.EXTENDED_POST_GIS) == "SRID=4326;POINTM (23.5732 25.3421 40.3)"

        # to get max a decimal precision
        print("G17  : " + point.as_text(WktVariant.ISO, NumericFormat.general(
            17)))  # POINT M (23.5732 25.342099999999999 40.299999999999997)
        assert point.as_text(WktVariant.ISO, NumericFormat.general(17)) == "POINT M (23.5732 25.342099999999999 40.299999999999997)"
        print("R    : " + point.as_text(WktVariant.ISO, NumericFormat.round_trip))  # POINT M (23.5732 25.3421 40.3)
        assert point.as_text(WktVariant.ISO, NumericFormat.round_trip) == "POINT M (23.5732 25.3421 40.3)"
        # to trim a decimal precision
        print("G3   : " + point.as_text(WktVariant.ISO, NumericFormat.general(3)))  # POINT M (23.6 25.3 40.3)
        assert point.as_text(WktVariant.ISO, NumericFormat.general(3)) == "POINT M (23.6 25.3 40.3)"
        print("Flat3: " + point.as_text(WktVariant.ISO, NumericFormat.flat(3)))  # POINT M (23.573 25.342 40.3)
        assert point.as_text(WktVariant.ISO, NumericFormat.flat(3)) == "POINT M (23.573 25.342 40.3)"

    def TranslateGeometryFromWkbTest(self):
        path = os.path.join(FolderSettings.CommonTestFolder(), "WkbFile.wkb")
        wkb = open(path, "rb").read()
        geometry = Geometry.from_binary(wkb)
        print(geometry.as_text())  # LINESTRING (1.2 3.4, 5.6 7.8)
        assert geometry.as_text() == "LINESTRING (1.2 3.4, 5.6 7.8)"

    def TranslateGeometryFromWktTest(self):
        line = Geometry.from_text("LINESTRING Z (0.1 0.2 0.3, 1 2 1, 12 23 2)")
        print(len(line))  # 3
        assert len(line) == 3

    def TranslateGeometryToWkbTest(self):
        path = os.path.join(FolderSettings.BaseTestOutputFolder(), "WkbFileOutput.wkb")
        referencePath = os.path.join(FolderSettings.CommonTestFolder(), "WkbFileOutput.wkb")
        geometry = Geometry.from_text("LINESTRING (1.2 3.4, 5.6 7.8)")
        wkb = geometry.as_binary()
        # with open(os.path.join(TestConfiguration.test_output_path, "file.wkb"), "wb") as f:
        with open(path, "wb") as f:
            f.write(wkb)

        Comparison.compare_binary_files(referencePath, path)

    def TranslateGeometryToWktTest(self):
        point = Point(23.5732, 25.3421)
        print(point.as_text())  # POINT (23.5732 25.3421)
        assert point.as_text() == "POINT (23.5732 25.3421)"