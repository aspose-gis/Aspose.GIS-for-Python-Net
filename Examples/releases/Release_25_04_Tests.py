import inspect
import io
import os
from uuid import UUID
import xml.etree.ElementTree as ET

import pytest
from aspose.gis import Drivers, VectorLayer, FeatureAttribute, AttributeDataType, GeoConvert, \
    PointFormats, AbstractPath, SavingOptions, AutoIds, Dataset
from aspose.gis.formats.filegdb import FileGdbOptions
from aspose.gis.formats.geojson import GeoJsonOptions
from aspose.gis.formats.gml import GmlOptions

from aspose.gis.formats.mapinfointerchange import MapInfoInterchangeOptions
from aspose.gis.geometries import Point, GeometryType
from aspose.gis.raster import RasterLayer, RasterRect
from aspose.gis.spatialreferencing import SpatialReferenceSystem
from datetime import datetime, time
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.FolderSettings import FolderSettings
from utils.LicenseHelper import LicenseHelper

class Release_25_04_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()


    initial_data = """{
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "id": 1,
                        "geometry": {
                            "type": "Point",
                            "coordinates": [-0.1276, 51.5072]
                        },
                        "properties": {
                            "name": "London",
                            "category": "city",
                            "population": 8982000,
                            "is_capital": true,
                            "description": "Capital of the United Kingdom"
                        }
                    },
                    {
                        "type": "Feature",
                        "id": 2,
                        "geometry": {
                            "type": "LineString",
                            "coordinates": [
                                [-0.1807, 51.4953],
                                [-0.1750, 51.5020],
                                [-0.1667, 51.5095]
                            ]
                        },
                        "properties": {
                            "name": "M25 Motorway",
                            "category": "highway",
                            "length_km": 188,
                            "lanes": 4
                        }
                    },
                    {
                        "type": "Feature",
                        "id": 3,
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [
                                [
                                    [-0.1637, 51.5079],
                                    [-0.1590, 51.5032],
                                    [-0.1523, 51.5058],
                                    [-0.1570, 51.5105],
                                    [-0.1637, 51.5079]
                                ]
                            ]
                        },
                        "properties": {
                            "name": "Hyde Park",
                            "category": "park",
                            "area_ha": 142,
                            "established": "1637-01-01"
                        }
                    },
                    {
                        "type": "Feature",
                        "id": 4,
                        "geometry": {
                            "type": "MultiPolygon",
                            "coordinates": [
                                [
                                    [
                                        [-0.0237, 51.5036],
                                        [-0.0200, 51.5000],
                                        [-0.0150, 51.5030],
                                        [-0.0237, 51.5036]
                                    ]
                                ],
                                [
                                    [
                                        [-0.0300, 51.5100],
                                        [-0.0250, 51.5080],
                                        [-0.0200, 51.5120],
                                        [-0.0300, 51.5100]
                                    ]
                                ]
                            ]
                        },
                        "properties": {
                            "name": "Canary Wharf Complex",
                            "category": "business district",
                            "status": "active",
                            "floors": 50,
                            "description": "Major financial hub in London"
                        }
                    }
                ]
            }"""

    xsd = """<?xml version="1.0" encoding="UTF-8"?>
        <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
                   xmlns:app="http://www.mydomain.net/myapp"
                   xmlns:gml="http://www.opengis.net/gml"
                   targetNamespace="http://www.mydomain.net/myapp"
                   elementFormDefault="qualified">

            <!-- Places (FeatureCollection override) -->
            <xs:element name="Places" type="app:PlacesType" 
                        substitutionGroup="gml:_FeatureCollection"/>

            <xs:complexType name="PlacesType">
                <xs:complexContent>
                    <xs:extension base="gml:AbstractFeatureCollectionType">
                        <xs:sequence>
                            <xs:element ref="app:placeMember" minOccurs="0" maxOccurs="unbounded"/>
                        </xs:sequence>
                    </xs:extension>
                </xs:complexContent>
            </xs:complexType>

            <!-- placeMember (featureMember override) -->
            <xs:element name="placeMember" type="app:PlaceMemberType"
                        substitutionGroup="gml:featureMember"/>

            <xs:complexType name="PlaceMemberType">
                <xs:complexContent>
                    <xs:extension base="gml:FeatureAssociationType">
                        <xs:sequence>
                            <xs:element ref="app:Place"/>
                        </xs:sequence>
                    </xs:extension>
                </xs:complexContent>
            </xs:complexType>

            <!-- Place (Feature override) -->
            <xs:element name="Place" type="app:PlaceType" 
                        substitutionGroup="gml:_Feature"/>

            <xs:complexType name="PlaceType">
                <xs:complexContent>
                    <xs:extension base="gml:AbstractFeatureType">
                        <xs:sequence>
                            <!-- Custom attributes -->
                            <xs:element name="id" type="xs:integer"/>                         
                            <xs:element name="name" type="xs:string"/>
                            <xs:element name="category" type="xs:string"/>
                            <!-- Geometry -->
                            <xs:element ref="gml:geometryProperty"/>
                        </xs:sequence>
                    </xs:extension>
                </xs:complexContent>
            </xs:complexType>

        </xs:schema>"""

    gml = """<?xml version="1.0" encoding="utf-8"?>
                <app:Places xmlns:gml="http://www.opengis.net/gml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:app="http://www.mydomain.net/myapp" xmlns:ogr="http://ogr.maptools.org/" xsi:schemaLocation="http://www.mydomain.net/myapp temp.xsd">
                  <app:placeMember>
                    <app:Place>
                      <app:name>London</app:name>
                      <app:category>city</app:category>
                      <app:id>1</app:id>
                      <gml:geometryProperty>
                        <gml:Point gml:srsName="http://www.opengis.net/gml/srs/epsg.xml#4326">
                          <gml:coord>
                            <gml:X>-0.1276</gml:X>
                            <gml:Y>51.5072</gml:Y>
                          </gml:coord>
                        </gml:Point>
                      </gml:geometryProperty>
                    </app:Place>
                  </app:placeMember>
                  <app:placeMember>
                    <app:Place>
                      <app:name>M25 Motorway</app:name>
                      <app:category>highway</app:category>
                      <app:id>2</app:id>
                      <gml:geometryProperty>
                        <gml:LineString gml:srsName="http://www.opengis.net/gml/srs/epsg.xml#4326">
                          <gml:coordinates xmlns:gml="http://www.opengis.net/gml" decimal="." cs="," ts=" ">-0.1807,51.4953 -0.175,51.502 -0.1667,51.5095</gml:coordinates>
                        </gml:LineString>
                      </gml:geometryProperty>
                    </app:Place>
                  </app:placeMember>
                  <app:placeMember>
                    <app:Place>
                      <app:name>Hyde Park</app:name>
                      <app:category>park</app:category>
                      <app:id>3</app:id>
                      <gml:geometryProperty>
                        <gml:Polygon gml:srsName="http://www.opengis.net/gml/srs/epsg.xml#4326">
                          <outerBoundaryIs>
                            <gml:LinearRing gml:srsName="http://www.opengis.net/gml/srs/epsg.xml#4326">
                              <gml:coordinates xmlns:gml="http://www.opengis.net/gml" decimal="." cs="," ts=" ">-0.1637,51.5079 -0.159,51.5032 -0.1523,51.5058 -0.157,51.5105 -0.1637,51.5079</gml:coordinates>
                            </gml:LinearRing>
                          </outerBoundaryIs>
                        </gml:Polygon>
                      </gml:geometryProperty>
                    </app:Place>
                  </app:placeMember>
                  <app:placeMember>
                    <app:Place>
                      <app:name>Canary Wharf Complex</app:name>
                      <app:category>business district</app:category>
                      <app:id>4</app:id>
                      <gml:geometryProperty>
                        <gml:MultiGeometry gml:srsName="http://www.opengis.net/gml/srs/epsg.xml#4326">
                          <gml:geometryMember>
                            <gml:Polygon gml:srsName="http://www.opengis.net/gml/srs/epsg.xml#4326">
                              <outerBoundaryIs>
                                <gml:LinearRing gml:srsName="http://www.opengis.net/gml/srs/epsg.xml#4326">
                                  <gml:coordinates xmlns:gml="http://www.opengis.net/gml" decimal="." cs="," ts=" ">-0.0237,51.5036 -0.02,51.5 -0.015,51.503 -0.0237,51.5036</gml:coordinates>
                                </gml:LinearRing>
                              </outerBoundaryIs>
                            </gml:Polygon>
                          </gml:geometryMember>
                          <gml:geometryMember>
                            <gml:Polygon gml:srsName="http://www.opengis.net/gml/srs/epsg.xml#4326">
                              <outerBoundaryIs>
                                <gml:LinearRing gml:srsName="http://www.opengis.net/gml/srs/epsg.xml#4326">
                                  <gml:coordinates xmlns:gml="http://www.opengis.net/gml" decimal="." cs="," ts=" ">-0.03,51.51 -0.025,51.508 -0.02,51.512 -0.03,51.51</gml:coordinates>
                                </gml:LinearRing>
                              </outerBoundaryIs>
                            </gml:Polygon>
                          </gml:geometryMember>
                        </gml:MultiGeometry>
                      </gml:geometryProperty>
                    </app:Place>
                  </app:placeMember>
                </app:Places>"""

    # Write data to GML Format
    # https://issue.saltov.dynabic.com/issues/GISNET-1194
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-17
    def GISNET1194Test(self):

        output_path = self.GetFileInOutputFolder("mapinfo.mif")
        ref_path = self.GetFileInBaseFolder("mapinfo.mif")

        standard_schematics_folder = os.path.join(self.GetBaseFolder(), "writing")
        #os.path.join(TestConfiguration.test_data_path, "gml", "writing") + os.sep
        app_scheme_path = self.GetFileInOutputFolder("temp.xsd")

        with open(app_scheme_path, "w") as f:
            f.write(self.xsd)

        input_stream = io.BytesIO(self.initial_data.encode("utf-8"))
        output_stream = io.BytesIO()

        with VectorLayer.open(AbstractPath.from_stream(input_stream), Drivers.geo_json) as lyr:
            layer = cast(VectorLayer, lyr)
            gml_options = GmlOptions()
            gml_options.application_namespace = "http://www.mydomain.net/myapp"

            # For .NET Core (Python equivalent)
            gml_options.schema_location = \
                f"http://www.w3.org/XML/1998/namespace { os.path.join(standard_schematics_folder, 'xml.xsd') }" + \
                f" http://www.w3.org/1999/xlink {standard_schematics_folder}\\xlink.xsd " + \
                f" http://www.opengis.net/gml {standard_schematics_folder}\\geometry.xsd " + \
                f" http://www.opengis.net/gml {standard_schematics_folder}\\feature.xsd " + \
                f" http://www.mydomain.net/myapp {app_scheme_path}"

            saving_options = SavingOptions()
            saving_options.driver_options = gml_options
            saving_options.spatial_reference_system = SpatialReferenceSystem.wgs84

            layer.save_to(AbstractPath.from_stream(output_stream), Drivers.gml, saving_options)

        output_stream.seek(0)

        # Compare XML documents
        expected_doc = ET.fromstring(self.gml.encode("utf-8"))
        actual_doc = ET.fromstring(output_stream.getvalue())

        if not self.elements_equal(expected_doc, actual_doc):
            assert False, "XML documents are not equal"

    def elements_equal(self, e1, e2):
        # Compare tag names
        if e1.tag != e2.tag:
            return False
        # Compare text content (ignoring whitespace)
        if (e1.text or "").strip() != (e2.text or "").strip():
            return False
        # Compare tail content (if relevant)
        if (e1.tail or "").strip() != (e2.tail or "").strip():
            return False
        # Compare attributes
        if e1.attrib != e2.attrib:
            return False
        # Compare number of children
        if len(e1) != len(e2):
            return False
        # Recursively compare all children
        return all(self.elements_equal(c1, c2) for c1, c2 in zip(e1, e2))

    # Support AutoId For SaveTo Method
    # https://issue.saltov.dynabic.com/issues/GISNET-1807
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-18
    def GISNET1807Test(self):
        # Create GeoJsonOptions with AutoId setting
        options = GeoJsonOptions()
        options.auto_id = AutoIds.NUMBER

        # Create a memory stream (in Python we'll use a file path or BytesIO)
        # Note: Aspose.GIS for Python may not directly support MemoryStream like C#
        # So we'll use a temporary file path for this example
        output_path = self.GetFileInOutputFolder("output.geojson")
        reference_path = self.GetFileInBaseFolder("output.geojson")

        # Create the vector layer
        with VectorLayer.create(output_path, Drivers.geo_json, options) as layer:
            # First feature
            f = layer.construct_feature()
            f.geometry = Point(10, 20)
            layer.add(f)

            # Second feature
            f = layer.construct_feature()
            f.geometry = Point(30, 40)
            layer.add(f)

        Comparison.compare_as_streams(output_path, reference_path)
        print("GeoJSON with IDs auto-update created successfully")

    # Add to Aspose.GIS support of BigTiff
    # https://issue.saltov.dynabic.com/issues/GISNET-1798
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-19
    def GISNET1798Test(self):
        input_path = self.GetFileInBaseFolder("bigtiff_resized.tif")
        # Open the GeoTIFF layer
        with Drivers.geo_tiff.open_layer(input_path) as lyr:
            layer = cast(RasterLayer, lyr)

            dump = layer.get_values_dump(RasterRect(0, 0, 688, 832))

            # Just random tests of dump
            assert -10000 == layer.no_data_values.as_integer(0)
            assert layer.no_data_values.as_integer(0) == dump[266].as_integer(0)
            assert abs(79.5961761474609 - dump[267].as_double(0)) < 0.000001
            assert abs(79.6245346069336 - dump[268].as_double(0)) < 0.000001

            # Assert SRS
            epsg_32611 = SpatialReferenceSystem.create_from_epsg(32611)
            assert str(epsg_32611) == str(layer.spatial_reference_system)
            assert epsg_32611.is_equivalent(layer.spatial_reference_system)

            # Assert Properties
            assert abs(402520.7656 - layer.upper_left_x) < 0.001
            assert abs(3765444.967 - layer.upper_left_y) < 0.001

            assert 1 == layer.band_count

            # band 0
            stats0 = layer.get_statistics(0, True)
            assert abs(96.760978698730469 - stats0.max) < 0.000001
            assert abs(73.536659240722656 - stats0.min) < 0.000001
            assert abs(80.511803399559511 - stats0.mean) < 0.000001
            assert abs(29675845.61504364 - stats0.sum) < 0.000001
            assert 368590 == stats0.count

            cell = layer.cell_size

            assert abs(0.74986191860469176 - cell.width) < 0.000001
            assert abs(0.75010661057715944 - cell.height) < 0.000001
            assert abs(0.74986191860469176 - cell.scale_x) < 0.000001
            assert abs(-0.75010661057715944 - cell.scale_y) < 0.000001
            assert abs(0.0 - cell.skew_x) < 0.000001
            assert abs(0.0 - cell.skew_y) < 0.000001

    # Fix For Writing Gdb File With HasZ (HasM) Options
    # https://issue.saltov.dynabic.com/issues/GISNET-1811
    # https://issue.saltov.dynabic.com/issues/GISPYTHON-20
    def GISNET1811Test(self):
        output_path = self.GetFileInOutputFolder("output.gdb")

        # Create dataset and layers
        with Dataset.create(output_path, Drivers.file_gdb) as dataset:
            # Create a layer without Z/M values
            options = FileGdbOptions()
            options.has_z = False
            options.has_m = False

            srs = SpatialReferenceSystem.wgs72
            with dataset.create_layer("point_layer", options, srs) as layer:
                feature = layer.construct_feature()
                feature.geometry = Point(1, 2)
                layer.add(feature)

            # Create a layer with Z/M values (default FileGdbOptions has Z/M enabled)
            with dataset.create_layer("point_ZM_layer", srs) as layer:
                feature = layer.construct_feature()
                feature.geometry = Point(1, 2, 3, 4)  # x, y, z, m
                layer.add(feature)

        # Verify the created dataset
        with Dataset.open(output_path, Drivers.file_gdb) as dataset:
            assert 2 == dataset.layers_count
            assert GeometryType.POINT == dataset.open_layer_at(0, None).geometry_type
            assert GeometryType.POINT == dataset.open_layer_at(1, None).geometry_type

            with dataset.open_layer("point_layer", None) as layer:
                assert 1 == layer.count
                expected_point = Point(1, 2)
                expected_point.spatial_reference_system = SpatialReferenceSystem.wgs72
                assert expected_point == layer[0].geometry

            with dataset.open_layer("point_ZM_layer", None) as layer:
                assert 1 == layer.count
                expected_point_zm = Point(1, 2, 3, 4)
                expected_point_zm.spatial_reference_system = SpatialReferenceSystem.wgs72
                assert expected_point_zm == layer[0].geometry