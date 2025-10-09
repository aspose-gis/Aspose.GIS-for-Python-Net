import hashlib
import math
from os import path

import pytest
from aspose.gis import Drivers, VectorLayer, Driver, Extent, Dataset, AbstractPath, DynamicFeature, NodeLink

from aspose.gis.geometries import Point, GeometryType, LineString, LinearRing, Polygon

from utils.BaseTests import BaseTests
from utils.LicenseHelper import LicenseHelper


class Release_25_09_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Ability to intersect huge shape files
    # https://issue.saltov.dynabic.com/issues/GISNET-683
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-42
    def GISNET683Test(self):
        # KML, GDB, ShapeFile, GeoJson and other format are supported
        driver = Drivers.kml  # Assuming enum mapping
        first_path = self.GetFileInOutputFolder("path_to_file1.kml")
        second_path = self.GetFileInOutputFolder("path_to_file2.kml")

        # Create first layer with polygons
        with driver.create_layer(first_path) as layer:
            for i in range(10):
                first_point_list = []
                first_point_list.append(Point(i * 10, 0))
                first_point_list.append(Point(i * 10 + 10, 0))
                first_point_list.append(Point(i * 10 + 10, 5))
                first_point_list.append(Point(i * 10, 5))
                first_point_list.append(Point(i * 10, 0))
                first_exterior_ring = LinearRing(first_point_list)
                polygon = Polygon(first_exterior_ring)
                feature = layer.construct_feature()
                feature.geometry = polygon
                layer.add(feature)

        # Create second layer with polygons
        with driver.create_layer(second_path) as layer:
            for i in range(50, 120):
                first_point_list = []
                first_point_list.append(Point(i + 1, 4))
                first_point_list.append(Point(i + 3, 4))
                first_point_list.append(Point(i + 3, 6))
                first_point_list.append(Point(i + 1, 6))
                first_point_list.append(Point(i + 1, 4))
                first_exterior_ring = LinearRing(first_point_list)
                polygon = Polygon(first_exterior_ring)
                feature = layer.construct_feature()
                feature.geometry = polygon
                layer.add(feature)

        # Perform intersection operations
        with driver.open_layer(first_path) as first_layer:
            with driver.open_layer(second_path) as second_layer:
                res_1 = first_layer.intersection_by_geometry(second_layer)
                res_2 = second_layer.intersection_by_geometry(first_layer)

                if res_1.count != 5 or res_2.count != 50:
                    raise Exception("Intersection was incorrect")

    # Ability to union extra complex geometries
    # https://issue.saltov.dynabic.com/issues/GISNET-814
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-45
    def GISNET814Test(self):
        point_list1 = []
        point_list1.append(Point(0, 0))
        point_list1.append(Point(10, 0))
        point_list1.append(Point(10, 5))
        point_list1.append(Point(0, 5))
        point_list1.append(Point(0, 0))
        exterior_ring1 = LinearRing(point_list1)
        geometry = Polygon(exterior_ring1)

        list_of_geometries = []
        for i in range(5):
            point_list2 = []
            point_list2.append(Point(i + 1, 4))
            point_list2.append(Point(i + 3, 4))
            point_list2.append(Point(i + 3, 6))
            point_list2.append(Point(i + 1, 6))
            point_list2.append(Point(i + 1, 4))
            exterior_ring2 = LinearRing(point_list2)
            list_of_geometries.append(Polygon(exterior_ring2))

        geom_after_union = geometry.union(list_of_geometries)

        expected_wkt = "POLYGON ((7 5, 10 5, 10 0, 0 0, 0 5, 1 5, 1 6, 2 6, 3 6, 4 6, 5 6, 6 6, 7 6, 7 5))"
        if (str(geom_after_union) != expected_wkt or geom_after_union.get_area() != 56):
            raise Exception("Incorrect Union")

#LicenseHelper.set_license()
#tests = Release_25_09_Tests()
#tests.GISNET814Test()